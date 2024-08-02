from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        # Check the event and webhook type
        event_type = data.get('type')
        webhook_type = data.get('webhookType')

        if webhook_type == 'taskActivity' and event_type == 'scored':
            # Check if the task was completed
            if data['direction'] == 'up' and data['task']['type'] == 'daily':
                task_id = data['task']['id']
                task_name = data['task']['text']
                print(f"Task completed: {task_name} (ID: {task_id})")
                return jsonify({"success": True, "message": "Task completion processed"}), 200
            else:
                return jsonify({"success": False, "message": "Task not completed"}), 400
        else:
            return jsonify({"success": False, "message": "Unsupported event type"}), 400
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app
    app.run(port=5000)
