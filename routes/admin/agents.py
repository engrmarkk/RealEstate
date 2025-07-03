from . import admin_blp
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required
from utils.util import (
    session_alert_bg_color,
    validate_correct_email,
    validate_phone_number,
)
from cruds import (
    get_all_agents,
    get_user_by_email,
    create_agent,
    get_user_by_phone,
    get_agent_by_id,
)
from logger import logger
from services.paystack import pay_stack
from connections.redis_connection import redis_conn
import json
from extensions import db


# all agents stats
@admin_blp.route("/agents")
@login_required
def all_agents_stats():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        alert, bg_color = session_alert_bg_color()
        agents, total_agents = get_all_agents(page, per_page)
        return render_template(
            "admin/agents.html",
            alert=alert,
            bg_color=bg_color,
            agents=agents,
            total_agents=total_agents,
        )
    except Exception as e:
        logger.error(f"Error getting all agents stats: {e}")
        return render_template(
            "admin/agents.html",
            alert=alert,
            bg_color=bg_color,
            agents=None,
            total_agents=None,
        )


@admin_blp.route("/view_agent/<string:agent_id>")
@login_required
def view_agent(agent_id):
    logger.info(f"Agent ID: {agent_id}")
    agent = get_agent_by_id(agent_id)
    alert, bg_color = session_alert_bg_color()
    banks = pay_stack.list_banks()
    return render_template(
        "admin/view_agent.html",
        agent=agent,
        banks=banks.get("data", []),
        alert=alert,
        bg_color=bg_color,
    )


# edit agent
@admin_blp.route("/edit_agent/<string:agent_id>", methods=["POST"])
@login_required
def edit_agent(agent_id):
    agent = get_agent_by_id(agent_id)

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    phone = request.form.get("phone")
    commission_rate = request.form.get("commission_rate")
    specialization = request.form.get("specialization")
    office_address = request.form.get("office_address")
    bank_code = request.form.get("bank_code")
    account_number = request.form.get("account_number")
    account_holder_name = request.form.get("account_holder_name")
    bank_name = request.form.get("bank_name")

    agent.user_profile.first_name = first_name or agent.user_profile.first_name
    agent.user_profile.last_name = last_name or agent.user_profile.last_name
    if phone and phone != agent.user_profile.phone:
        phone_res = validate_phone_number(phone)
        if phone_res:
            session_alert_bg_color(phone_res)
            return redirect(url_for("admin_blp.view_agent", agent_id=agent_id))
        if get_user_by_phone(phone):
            session_alert_bg_color("Phone number already exists")
            return redirect(url_for("admin_blp.view_agent", agent_id=agent_id))
        agent.user_profile.phone = phone or agent.user_profile.phone
    agent.agent.commission_rate = commission_rate or agent.agent.commission_rate
    agent.agent.specialization = specialization or agent.agent.specialization
    agent.agent.office_address = office_address or agent.agent.office_address

    agent_bnk_details = agent.agent.agent_bank_details
    agent_bnk_details.bank_code = bank_code or agent_bnk_details.bank_code
    agent_bnk_details.account_number = (
        account_number or agent_bnk_details.account_number
    )
    agent_bnk_details.account_holder_name = (
        account_holder_name or agent_bnk_details.account_holder_name
    )
    agent_bnk_details.bank_name = bank_name or agent_bnk_details.bank_name

    db.session.commit()
    return redirect(url_for("admin_blp.view_agent", agent_id=agent_id))


# add_agent
@admin_blp.route("/add_agent", methods=["GET", "POST"])
@login_required
def add_agent():
    from workers.utils.cel_workers import send_mail

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        license_number = request.form.get("license_number")
        experience_years = request.form.get("experience_years")
        commission_rate = request.form.get("commission_rate")
        bank_code = request.form.get("bank_code")
        bank_code_text = request.form.get("bank_code_text")
        account_number = request.form.get("account_number")
        account_holder_name = request.form.get("account_holder_name")
        bank_name = request.form.get("bank_name")

        red_dict = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "license_number": license_number,
            "experience_years": experience_years,
            "commission_rate": commission_rate,
            "bank_code": bank_code,
            "bank_code_text": bank_code_text,
            "account_number": account_number,
            "account_holder_name": account_holder_name,
            "bank_name": bank_name,
        }

        def add_json_to_redis():
            redis_conn.set("add_agent", json.dumps(red_dict), 10)

        if not all(
            [
                first_name,
                last_name,
                email,
                phone,
                license_number,
                experience_years,
                commission_rate,
                bank_code,
                bank_code_text,
                account_number,
                account_holder_name,
                bank_name,
            ]
        ):
            add_json_to_redis()
            session_alert_bg_color("All fields are required")
            return redirect(url_for("admin_blp.add_agent"))

        email_res = validate_correct_email(email)
        if not email_res[0]:
            add_json_to_redis()
            session_alert_bg_color(email_res[1])
            return redirect(url_for("admin_blp.add_agent"))

        email = email_res[1]

        phone_res = validate_phone_number(phone)
        if phone_res:
            add_json_to_redis()
            session_alert_bg_color(phone_res)
            return redirect(url_for("admin_blp.add_agent"))

        if get_user_by_phone(phone):
            add_json_to_redis()
            session_alert_bg_color("Phone number already exists")
            return redirect(url_for("admin_blp.add_agent"))

        if get_user_by_email(email):
            add_json_to_redis()
            session_alert_bg_color("Email already exists")
            return redirect(url_for("admin_blp.add_agent"))

        user = create_agent(
            first_name,
            last_name,
            email,
            license_number,
            experience_years,
            commission_rate,
            bank_code,
            account_number,
            account_holder_name,
            bank_name,
            phone,
        )

        if not user:
            add_json_to_redis()
            session_alert_bg_color("Error creating agent")
            return redirect(url_for("admin_blp.add_agent"))

        redis_conn.delete("add_agent")
        session_alert_bg_color("Agent created successfully", "green")

        send_mail.delay(
            {
                "subject": "Agent Created",
                "template_name": "agent_created.html",
                "email": email,
                "first_name": first_name.title(),
                "last_name": last_name.title(),
            }
        )

        return redirect(url_for("admin_blp.add_agent"))
    alert, bg_color = session_alert_bg_color()
    banks = pay_stack.list_banks()
    agent_fields = redis_conn.get("add_agent")
    agent_fields = json.loads(agent_fields) if agent_fields else {}
    return render_template(
        "admin/add_agent.html",
        alert=alert,
        bg_color=bg_color,
        banks=banks.get("data", []),
        first_name=agent_fields.get("first_name", ""),
        last_name=agent_fields.get("last_name", ""),
        email=agent_fields.get("email", ""),
        phone=agent_fields.get("phone", ""),
        license_number=agent_fields.get("license_number", ""),
        experience_years=agent_fields.get("experience_years", ""),
        commission_rate=agent_fields.get("commission_rate", ""),
        bank_code=agent_fields.get("bank_code", ""),
        bank_code_text=agent_fields.get("bank_code_text", ""),
        account_number=agent_fields.get("account_number", ""),
        account_holder_name=agent_fields.get("account_holder_name", ""),
        bank_name=agent_fields.get("bank_name", ""),
    )
