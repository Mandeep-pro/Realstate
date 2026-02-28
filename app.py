### put and delete https - verbs
### working with API's-- Json

from flask import Flask, jsonify, request   
app = Flask(__name__)

## initial data in todo list
todos = [
    {"id": 1, "task": "Buy groceries", "status": "pending"},
    {"id": 2, "task": "Clean the house", "status": "pending"},
    {"id": 3, "task": "Finish project", "status": "pending"}    

]
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

## retrieve all the items in the todo list
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)


## get: Retrieve a specific item by ID
@app.route('/todos/<int:todo_id>', methods=['GET']) 
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        return jsonify(todo)
    else:
        return jsonify({"error": "Todo not found"}), 404        
    return jsonify(todo)

## post: Add a new item to the todo list
@app.route('/todos', methods=['POST'])  
def add_todo():
    new_todo = request.get_json()
    new_todo['id'] = len(todos) + 1
    todos.append(new_todo)
    return jsonify(new_todo)
## put: Update an existing item by ID
@app.route('/todos/<int:todo_id>', methods=['PUT']) 
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    updated_data = request.get_json()
    todo.update(updated_data)
    return jsonify(todo)    



## delete: Remove an item by ID
@app.route('/todos/<int:todo_id>', methods=['DELETE'])          
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({"message": "Todo deleted successfully"})    





if __name__ == '__main__':
    app.run(debug=True)