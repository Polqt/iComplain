import { writable, type Readable } from "svelte/store";
import type { CommentsState, TicketComment } from "../types/comments.ts";

interface CommentsStore extends Readable<CommentsState> {
    setComments: (comments: TicketComment[]) => void;
    // TODO: Define methods for managing comments
    // Example: loadCommentsForTicket: (ticketId: number) => Promise<void>;
    // Example: createComment: (ticketId: number, content: string) => Promise<Comment>;
    // You may base these method on ticket store methods, but adapt them for comments
}


// TODO: Implement the comments store with methods to manage comments, similar to the tickets store
// Base the implementation on the structure of the tickets store, but adapt it for handling comments instead of tickets
// Connected to the interface defined above, and ensure it can manage the state of comments effectively, including loading, creating, updating, and deleting comments as needed.

// function createeComentsStore(): CommentsStore {
// }