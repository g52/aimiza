from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import openai
import datetime
from models import db, User, Goal, Progress

app = Flask(__name__)
app.config.from_object('config')  # This will load your database configurations from config.py
db.init_app(app)

# Set up JWT
jwt = JWTManager(app)

# OpenAI API key setup (ensure you have access to the GPT API)
openai.api_key = 'your-openai-api-key'  # Replace with your actual OpenAI API key

# Endpoint to generate AI-based recommendations for goals
def generate_recommendation(goal_description, current_value, target):
    prompt = f"Provide a personalized recommendation for a health behavioral goal. The goal description is '{goal_description}', the current value is {current_value}, and the target value is {target}. What are the next steps the user should take?"

    response = openai.Completion.create(
        engine="text-davinci-003",  # Change to your preferred model, e.g., GPT-4
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify(message="Invalid credentials"), 401

# Create Goal Route
@app.route('/create_goal', methods=['POST'])
@jwt_required()
def create_goal():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    goal = Goal(description=data['description'], target=data['target'], user_id=current_user_id)
    
    # Generate AI recommendation for the goal
    recommendation = generate_recommendation(data['description'], 0, data['target'])
    
    # Save the goal with the generated recommendation
    goal.recommendation = recommendation
    
    db.session.add(goal)
    db.session.commit()
    
    return jsonify(message="Goal created successfully", recommendation=recommendation), 201

# Update Progress Route
@app.route('/update_progress', methods=['POST'])
@jwt_required()
def update_progress():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    goal = Goal.query.filter_by(id=data['goal_id'], user_id=current_user_id).first()

    if goal:
        progress = Progress(value=data['value'], goal_id=goal.id)
        goal.current_value = data['value']
        goal.progress = (goal.current_value / goal.target) * 100
        
        # Generate updated recommendation based on new progress
        recommendation = generate_recommendation(goal.description, goal.current_value, goal.target)
        goal.recommendation = recommendation
        
        db.session.add(progress)
        db.session.commit()
        
        return jsonify(message="Progress updated successfully", recommendation=recommendation), 200
    return jsonify(message="Goal not found"), 404

# Session Summary Route
@app.route('/session_summary', methods=['GET'])
@jwt_required()
def session_summary():
    current_user_id = get_jwt_identity()
    goal_id = request.args.get('goal_id')
    
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user_id).first()
    if goal:
        latest_progress = Progress.query.filter_by(goal_id=goal.id).order_by(Progress.session_date.desc()).first()
        if latest_progress:
            return jsonify({
                'session_date': latest_progress.session_date,
                'value': latest_progress.value,
                'recommendation': goal.recommendation
            }), 200
    return jsonify(message="Progress not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
