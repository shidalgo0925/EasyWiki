# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from ..extensions import get_db, get_current_user_id
from ..models.decisions import Decision
from ..models.roadmap_items import RoadmapItem

strategy_bp = Blueprint("strategy", __name__, url_prefix="/strategy")


# --- Decisiones ---

@strategy_bp.route("/decisions")
def decisions_list():
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión", "warning")
        return redirect(url_for("auth.login"))
    db = get_db()
    items = db.query(Decision).filter(
        Decision.user_id == user_id,
        Decision.estado != "archivada"
    ).order_by(Decision.decision_date.desc()).all()
    return render_template("strategy/decisions.html", items=items)


@strategy_bp.route("/decisions/new", methods=["POST"])
def decision_new():
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))
    db = get_db()
    d = Decision(
        user_id=user_id,
        title=request.form.get("title", "").strip(),
        contexto=request.form.get("contexto"),
        impacto=request.form.get("impacto"),
        decision_date=date.fromisoformat(request.form.get("decision_date")) if request.form.get("decision_date") else date.today(),
        review_date=date.fromisoformat(request.form.get("review_date")) if request.form.get("review_date") else None,
    )
    db.add(d)
    db.commit()
    flash("Decisión registrada", "success")
    return redirect(url_for("strategy.decisions_list"))


@strategy_bp.route("/decisions/<int:id>/update", methods=["POST"])
def decision_update(id):
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))
    db = get_db()
    d = db.query(Decision).filter(Decision.id == id, Decision.user_id == user_id).first()
    if not d:
        flash("Decisión no encontrada", "danger")
        return redirect(url_for("strategy.decisions_list"))
    d.estado = request.form.get("estado", d.estado)
    d.review_date = date.fromisoformat(request.form.get("review_date")) if request.form.get("review_date") else d.review_date
    db.commit()
    flash("Decisión actualizada", "success")
    return redirect(url_for("strategy.decisions_list"))


# --- Roadmap ---

@strategy_bp.route("/roadmap")
def roadmap_list():
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión", "warning")
        return redirect(url_for("auth.login"))
    db = get_db()
    items = db.query(RoadmapItem).filter(
        RoadmapItem.user_id == user_id,
        RoadmapItem.estado != "completado"
    ).order_by(RoadmapItem.prioridad.asc(), RoadmapItem.created_at.desc()).all()
    return render_template("strategy/roadmap.html", items=items)


@strategy_bp.route("/roadmap/new", methods=["POST"])
def roadmap_new():
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))
    db = get_db()
    r = RoadmapItem(
        user_id=user_id,
        nombre=request.form.get("nombre", "").strip(),
        descripcion=request.form.get("descripcion"),
        prioridad=int(request.form.get("prioridad", 2)),
        estado=request.form.get("estado", "planeado"),
        proxima_accion=request.form.get("proxima_accion"),
        bloqueado_por=request.form.get("bloqueado_por"),
        fecha_objetivo=date.fromisoformat(request.form.get("fecha_objetivo")) if request.form.get("fecha_objetivo") else None,
    )
    db.add(r)
    db.commit()
    flash("Item de roadmap agregado", "success")
    return redirect(url_for("strategy.roadmap_list"))


@strategy_bp.route("/roadmap/<int:id>/update", methods=["POST"])
def roadmap_update(id):
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for("auth.login"))
    db = get_db()
    r = db.query(RoadmapItem).filter(RoadmapItem.id == id, RoadmapItem.user_id == user_id).first()
    if not r:
        flash("Item no encontrado", "danger")
        return redirect(url_for("strategy.roadmap_list"))
    r.estado = request.form.get("estado", r.estado)
    r.prioridad = int(request.form.get("prioridad", r.prioridad))
    r.proxima_accion = request.form.get("proxima_accion", r.proxima_accion)
    r.bloqueado_por = request.form.get("bloqueado_por", r.bloqueado_por)
    db.commit()
    flash("Roadmap actualizado", "success")
    return redirect(url_for("strategy.roadmap_list"))