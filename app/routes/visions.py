# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from ..extensions import get_db, get_current_user_id
from ..models.visions import Vision
from ..models.areas import Area
from ..models.projects import Project
from ..models.objectives import Objective

visions_bp = Blueprint("visions", __name__, url_prefix="/visions")


@visions_bp.route("/")
def list_visions():
    db = get_db()
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión primero", "warning")
        return redirect(url_for("auth.login"))
    visions = db.query(Vision).filter(Vision.user_id == user_id, Vision.is_active == True).order_by(Vision.created_at.desc()).all()
    return render_template("visions/list.html", visions=visions)


@visions_bp.route("/new", methods=["GET", "POST"])
def new_vision():
    db = get_db()
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión primero", "warning")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        vision = Vision(
            user_id=user_id,
            titulo=request.form.get("titulo"),
            descripcion=request.form.get("descripcion"),
            horizonte=request.form.get("horizonte", "5y"),
            color=request.form.get("color", "#1f6feb"),
        )
        db.add(vision)
        db.commit()
        flash("Visión creada", "success")
        return redirect(url_for("visions.list_visions"))
    return render_template("visions/form.html", vision=None)


@visions_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_vision(id):
    db = get_db()
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión primero", "warning")
        return redirect(url_for("auth.login"))
    vision = db.query(Vision).filter(Vision.id == id, Vision.user_id == user_id).first()
    if not vision:
        flash("Visión no encontrada", "danger")
        return redirect(url_for("visions.list_visions"))
    if request.method == "POST":
        vision.titulo = request.form.get("titulo")
        vision.descripcion = request.form.get("descripcion")
        vision.horizonte = request.form.get("horizonte", "5y")
        vision.color = request.form.get("color", "#1f6feb")
        db.commit()
        flash("Visión actualizada", "success")
        return redirect(url_for("visions.list_visions"))
    return render_template("visions/form.html", vision=vision)


@visions_bp.route("/<int:id>/delete", methods=["POST"])
def delete_vision(id):
    db = get_db()
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión primero", "warning")
        return redirect(url_for("auth.login"))
    vision = db.query(Vision).filter(Vision.id == id, Vision.user_id == user_id).first()
    if vision:
        vision.is_active = False
        db.commit()
        flash("Visión eliminada", "info")
    return redirect(url_for("visions.list_visions"))


@visions_bp.route("/<int:id>")
def view_vision(id):
    db = get_db()
    user_id = get_current_user_id()
    if not user_id:
        flash("Inicia sesión primero", "warning")
        return redirect(url_for("auth.login"))
    vision = db.query(Vision).filter(Vision.id == id, Vision.user_id == user_id, Vision.is_active == True).first()
    if not vision:
        flash("Visión no encontrada", "danger")
        return redirect(url_for("visions.list_visions"))
    areas = db.query(Area).filter(Area.vision_id == id, Area.is_active == True).order_by(Area.orden.asc()).all()
    return render_template("visions/view.html", vision=vision, areas=areas)