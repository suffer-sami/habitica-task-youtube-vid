import json
import logging
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from .youtube import get_latest_video
from .whatsapp import send_whatsapp_message
from .config import Config


webhook_bp = Blueprint('webhook', __name__)


def process_task_completion():
    """Process the task completion."""
    latest_video = get_latest_video()
    logging.info(latest_video)
    if latest_video and Config.SEND_WHATSAPP_MESSAGES:
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

        log_data = {
            "event_type": event_type,
            "webhook_type": webhook_type,
            "task_type": task_type,
            "task_name": task_name,
            "direction": direction
        }
        logging.info("Received webhook: %s", json.dumps(log_data, indent=4))

        if (
            webhook_type == 'taskActivity' and
            event_type == 'scored' and
            task_type == 'daily' and
            direction == 'up' and
            task_name == Config.TASK_TO_BE_COMPLETED
        ):
            return jsonify(process_task_completion()), 200

        logging.info("No action required for this webhook")
        return jsonify({"success": True, "message": "No action required"}), 200

    except BadRequest as e:
        logging.warning(f"Bad request: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500
