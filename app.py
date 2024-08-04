import logging
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            raise BadRequest("No JSON data received")

        event_type = data.get('type')
        webhook_type = data.get('webhookType')

        if webhook_type == 'taskActivity' and event_type == 'scored':
            task = data.get('task', {})
            task_type = task.get('type')
            task_name = task.get('text')
            direction = data.get('direction')

            app.logger.info(f"Task type: {task_type}, Task name: {task_name}, Direction: {direction}")

            if task_type == 'daily' and direction == 'up' and task_name == "Goto Walk":
                app.logger.info("Processing 'Goto Walk' task completion")
                return jsonify({"success": True, "message": "Task completion processed"}), 200

        app.logger.info("No action required for this webhook")
        return jsonify({"success": True, "message": "No action required"}), 200
    
    except BadRequest as e:
        app.logger.warning(f"Bad request: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(port=5000)
