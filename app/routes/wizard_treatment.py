# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, session

from app.services.treatment_service import (
    get_active_treatment,
    get_latest_draft,
    build_prefill,
    treatment_to_dict,
)

treatment_wizard_bp = Blueprint("treatment_wizard", __name__, url_prefix="/wizard")


@treatment_wizard_bp.get("/treatment")
def treatment_wizard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    active = get_active_treatment(user_id)
    draft = get_latest_draft(user_id)
    prefill = build_prefill(user_id)

    initial = treatment_to_dict(draft) if draft else {}
    profile_id = draft.id if draft else None

    if not initial and active:
        initial = treatment_to_dict(active)
        # No reutilizar ID del activo: nuevo borrador al guardar
        profile_id = None

    return render_template(
        "wizard_treatment.html",
        active_treatment=active,
        initial_data=initial,
        prefill=prefill,
        profile_id=profile_id,
    )
