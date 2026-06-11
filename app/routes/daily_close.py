# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from ..extensions import get_db, get_current_user_id
from ..models.daily_focus import DailyFocus, FocusItem
from ..models.daily_reflections import DailyReflection
from ..models.wins import Win

daily_close_bp = Blueprint("daily_close", __name__, url_prefix="/daily")


@daily_close_bp.route("/close", methods=["GET", "POST"])
def close():
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión para cerrar tu día", "warning")
        return redirect(url_for("auth.login"))

    db = get_db()
    today = date.today()

    # Buscar DailyFocus del día
    daily = db.query(DailyFocus).filter(
        DailyFocus.user_id == user_id,
        DailyFocus.fecha == today
    ).first()

    # Reflexión existente
    reflection = db.query(DailyReflection).filter(
        DailyReflection.user_id == user_id,
        DailyReflection.fecha == today
    ).first()

    # Wins del día
    wins = db.query(Win).filter(
        Win.user_id == user_id,
        Win.fecha == today
    ).all()

    if request.method == "POST":
        try:
            # Buscar o crear DailyFocus
            if not daily:
                daily = DailyFocus(user_id=user_id, fecha=today)
                db.add(daily)
                db.flush()

            # Marcar FocusItem completados
            completed_ids = request.form.getlist("completed_items")
            if daily:
                for item in daily.items:
                    item.estado = "completada" if str(item.id) in completed_ids else item.estado
                    if str(item.id) in completed_ids and not item.completed_at:
                        from datetime import datetime
                        item.completed_at = datetime.now()

            # Crear o actualizar reflexión
            if reflection:
                reflection.que_funciono = request.form.get("que_funciono")
                reflection.que_bloqueo = request.form.get("que_bloqueo")
                reflection.aprendizaje = request.form.get("aprendizaje")
                reflection.ajuste_manana = request.form.get("ajuste_manana")
                reflection.estado_animo = request.form.get("estado_animo")
                energia = request.form.get("energia_final")
                reflection.energia_final = int(energia) if energia else None
                reflection.daily_focus_id = daily.id if daily else None
            else:
                new_reflection = DailyReflection(
                    user_id=user_id,
                    daily_focus_id=daily.id if daily else None,
                    fecha=today,
                    que_funciono=request.form.get("que_funciono"),
                    que_bloqueo=request.form.get("que_bloqueo"),
                    aprendizaje=request.form.get("aprendizaje"),
                    ajuste_manana=request.form.get("ajuste_manana"),
                    estado_animo=request.form.get("estado_animo"),
                    energia_final=int(request.form.get("energia_final")) if request.form.get("energia_final") else None,
                )
                db.add(new_reflection)

            # Crear win si se envió
            win_titulo = request.form.get("win_titulo", "").strip()
            if win_titulo:
                new_win = Win(
                    user_id=user_id,
                    daily_focus_id=daily.id if daily else None,
                    fecha=today,
                    titulo=win_titulo,
                    descripcion=request.form.get("win_descripcion"),
                    impacto=request.form.get("win_impacto", "medio"),
                )
                db.add(new_win)

            db.commit()
            flash("Cierre diario guardado correctamente", "success")
            return redirect(url_for("dashboard.dashboard"))

        except Exception as e:
            db.rollback()
            flash(f"Error al guardar: {str(e)}", "danger")

    return render_template(
        "daily/close.html",
        daily=daily,
        items=daily.items if daily else [],
        reflection=reflection,
        wins=wins,
        today=today.isoformat(),
    )