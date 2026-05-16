"""Africa's Talking Webhook Handlers."""

from fastapi import APIRouter, Request, Response
from src.gateway.normalizer import normalize_sms, normalize_ussd, normalize_whatsapp
from src.gateway.formatter import format_response
from src.agents.runner import process_message
from src.gateway.at_service import send_sms, send_whatsapp

router = APIRouter(prefix="/webhook", tags=["webhooks"])

@router.post("/sms")
async def sms_webhook(request: Request):
    form_data = dict(await request.form())
    envelope = normalize_sms(form_data)
    response_text = await process_message(envelope)
    formatted = format_response(response_text, "sms")
    send_sms(form_data.get("from", ""), formatted)
    return {"status": "ok"}

@router.post("/ussd")
async def ussd_webhook(request: Request):
    form_data = dict(await request.form())
    envelope = normalize_ussd(form_data)
    # USSD usually starts with empty text
    if not envelope.text:
        menu = "Welcome to Sauti ya Mwananchi\n1. Rights\n2. Station\n3. Fact Check"
        return Response(content=format_response(menu, "ussd", end_session=False), media_type="text/plain")
    
    response_text = await process_message(envelope)
    return Response(content=format_response(response_text, "ussd"), media_type="text/plain")

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = dict(await request.form())
    envelope = normalize_whatsapp(form_data)
    response_text = await process_message(envelope)
    formatted = format_response(response_text, "whatsapp")
    send_whatsapp(form_data.get("from", ""), formatted)
    return {"status": "ok"}
