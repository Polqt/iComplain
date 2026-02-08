import type { User } from "./user.ts";

export type Category = {
    id: number;
    name: string;
}

export type Priority = {
    id: number;
    name: string;
}

export type Ticket = {
    id: number;
    title: string;
    student: User;
    category: Category;
    priority: Priority;
    building: string;
    room_name: string;
    status: string;
    created_at: string;
    updated_at: string;
    ticket_number: string;
}