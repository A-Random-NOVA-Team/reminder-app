// Use ISO 8601 format for date strings!!
export type Task = {
    id: string;
    name: string;
    description: string | null;
    due_date: string | null;
    is_completed: boolean;

    diffulty_score: number | null;
    reasoning: string | null;
    diffulty_estimation_time: string | null;

    create_time: string;
    update_time: string;
};

export type CreateTaskRequest = {
    name: string;
    description: string | null;
    due_date: string | null;
};

export type UpdateTaskRequest = {
    name?: string;
    description?: string | null;
    due_date?: string | null;
    is_completed?: boolean;
    difficulty_reestimate?: boolean;
};
