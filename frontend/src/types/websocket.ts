export type WSStatus = "connected" | "disconnected" | "connecting";

export type WSMessage = {
    action?: string;
    type?: string;
    ticket_id?: number;
    comment?: any;
    message?: string;
    notification?: any;
};