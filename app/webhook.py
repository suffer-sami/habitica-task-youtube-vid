import logging
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from .youtube import get_latest_video
from .whatsapp import send_whatsapp_message

webhook_bp = Blueprint('webhook', __name__)

def process_goto_walk_task():
    """Process the 'Goto Walk' task completion."""
    latest_video = get_latest_video()
    logging.info(latest_video)
    if latest_video:
        message_id = send_whatsapp_message(f"🎁: {latest_video}")
        logging.info(f"Message Sent (ID: {message_id})")
    return {"success": True, "message": "Task completion processed"}

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            raise BadRequest("No JSON data received")

        event_type = data.get('type')
        webhook_type = data.get('webhookType')
        task = data.get('task', {})
        task_type = task.get('type')
        task_name = task.get('text')
        direction = data.get('direction')

        logging.info(f"Received webhook - Event: {event_type}, Webhook: {webhook_type}, Task: {task_type}, Name: {task_name}, Direction: {direction}")

        if webhook_type == 'taskActivity' and event_type == 'scored' and task_type == 'daily' and direction == 'up' and task_name == "Goto Walk":
            return jsonify(process_goto_walk_task()), 200

        logging.info("No action required for this webhook")
        return jsonify({"success": True, "message": "No action required"}), 200

    except BadRequest as e:
        logging.warning(f"Bad request: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({"success": False, "message": "Internal server error"}), 500