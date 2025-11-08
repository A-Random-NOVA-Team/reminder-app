import { Task, CreateTaskRequest, UpdateTaskRequest } from './types';

const API_BASE_URL = 'http://localhost:8000'; // TODO!

export async function getTasks(excludeCompleted: boolean = false): Promise<Task[]> {
    const url = `${API_BASE_URL}/tasks?exclude_completed=${excludeCompleted}`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.statusText}`);
    }
    const data: Task[] = await response.json();
    return data;
}

/**
 * Creates a new task.
 */
export async function createTask(data: CreateTaskRequest): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (response.status !== 201) {
        throw new Error(`Failed to create task: ${response.statusText}`);
    }
    const task: Task = await response.json();
    return task;
}

/**
 * Updates an existing task.
 */
export async function updateTask(taskId: string, data: UpdateTaskRequest): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error(`Failed to update task: ${response.statusText}`);
    }
    const task: Task = await response.json();
    return task;
}

/**
 * Deletes a task.
 */
export async function deleteTask(taskId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'DELETE',
    });
    if (response.status !== 204) {
        throw new Error(`Failed to delete task: ${response.statusText}`);
    }
}
