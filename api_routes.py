from bottle import route, request, response
import json
from datetime import datetime

import database
import global_defs

@route('/api/update_realtime', method='POST')
def update_realtime():
    try:
        data = request.json
        data_type = data.get('type')
        form_data = data.get('data')
        
        if data_type == 'login':
            global_defs.PYTHON_GLOBAL_DATA['login_data'] = form_data
        elif data_type == 'register':
            global_defs.PYTHON_GLOBAL_DATA['reg_data'] = form_data
        elif data_type == 'opros':
            global_defs.PYTHON_GLOBAL_DATA['opros_data'] = form_data
        
        global_defs.PYTHON_GLOBAL_DATA['last_update'] = datetime.now().isoformat()
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@route('/api/get_global_data')
def get_global_data():
    response.content_type = 'application/json'
    return json.dumps(global_defs.PYTHON_GLOBAL_DATA)

@route('/api/get_tasks')
def get_tasks_api():
    response.content_type = 'application/json'
    tasks = database.db.get_tasks()
    return json.dumps({'tasks': tasks})

@route('/api/get_task/<task_id:int>')
def get_task_api(task_id):
    response.content_type = 'application/json'
    task = database.db.get_task_by_id(task_id)
    if task:
        return json.dumps({'task': task})
    return json.dumps({'error': 'Task not found'})

@route('/api/admin/insert_test_data', method='POST')
def api_insert_test_data():
    success = database.db.insert_test_data()
    if success:
        return '''
        <script>
            alert("Test data inserted successfully!");
            window.location.href = "/";
        </script>
        '''
    else:
        return '''
        <script>
            alert("Error inserting test data!");
            window.location.href = "/";
        </script>
        '''

@route('/api/admin/clear_data', method='POST')
def api_clear_data():
    success = database.db.clear_all_data()
    if success:
        return '''
        <script>
            alert("All data cleared successfully!");
            window.location.href = "/";
        </script>
        '''
    else:
        return '''
        <script>
            alert("Error clearing data!");
            window.location.href = "/";
        </script>
        '''

@route('/api/admin/stats')
def api_database_stats():
    response.content_type = 'application/json'
    stats = database.db.get_database_stats()
    return json.dumps({
        'success': True,
        'stats': stats,
        'timestamp': datetime.now().isoformat()
    })