import { PUBLIC_API_URL } from "$env/static/public";
import { writable } from "svelte/store";
import type { WSMessage, WSStatus } from "../types/websocket.ts";
import { ticketsStore } from "./tickets.store.ts";
import { commentsStore } from "./comment.store.ts";

function createWebSocketStore() {
    const { subscribe, set } = writable<WSStatus>("disconnected");
    let socket: WebSocket | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    let reconnectAttempts = 0;
    const MAX_RECONNECT_ATTEMPTS = 10;
    const BASE_DELAY = 1000;

    function getWsUrl(): string {
        const url = new URL(PUBLIC_API_URL)
        const protocol = url.protocol === "https:" ? "wss:" : "ws:";
        return `${protocol}//${url.host}/ws/tickets/`;
    }

    function connect() {
        if (socket?.readyState === WebSocket.OPEN) {
            console.log("WebSocket already connected");
            return;
        }

        set("connecting");
        const wsUrl = getWsUrl();
        console.log(`Connecting to WebSocket at ${wsUrl}`);

        try {
            socket = new WebSocket(wsUrl);

            socket.onopen = () => {
                console.log("WebSocket connected");
                set("connected");
                reconnectAttempts = 0;
                if (reconnectTimer) {
                    clearTimeout(reconnectTimer);
                    reconnectTimer = null;
                }
            };

            socket.onmessage = (event) => {
                handleMessage(event);
            };

            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
            }
            
            socket.onclose = (event) => {
                set("disconnected");
                socket = null;
                
                if (event.code !== 1000) {
                    scheduleReconnect();
                }
            }
        } catch (error) {
            console.error("Failed to connect to WebSocket:", error);
            set("disconnected");
            scheduleReconnect();
        }


    }

    function handleMessage(event: MessageEvent) {
        try {
            const data: WSMessage =JSON.parse(event.data);
            console.log("Websocket message received:", data);

            // Handle ticket updates
            if (data.action === "created") {
                ticketsStore.loadTickets();
            } else if (data.action === "updated") {
                if (data.ticket_id) {
                    ticketsStore.loadTicketById(data.ticket_id)
                }
            } else if (data.action === "deleted") {
                if (data.ticket_id) {
                    ticketsStore.removeTicketFromStore(data.ticket_id);
                }
            }

            // Handle comment updates
            if (data.type === "comment_created") {
                if (data.ticket_id && data.comment) {
                    commentsStore.addCommentToStore(data.comment);
                }
            } else if (data.type === "comment_updated") {
                if (data.comment) {
                    commentsStore.updateCommentInStore(data.comment.id, { message: data.comment.message });
                }
            } else if (data.type === "comment_deleted") {
                if (data.comment) {
                    commentsStore.removeCommentFromStore(data.comment.id);
                }
            }

            // Handle feedbacks updates

        } catch (error) {
            console.error("Failed to parse WebSocket message:", error);
        }
    }

    function scheduleReconnect() {
        if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
            console.log("Max reconnect attempts reached. Giving up.");
            return;
        }

        if (reconnectTimer) {
            clearTimeout(reconnectTimer);
        }
        
        const delay = Math.min(
            BASE_DELAY * Math.pow(2, reconnectAttempts),
            30000
        );

        reconnectAttempts++;
        console.log(`WebSocket disconnected. Attempting to reconnect in ${delay / 1000} seconds... (Attempt ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`);
        reconnectTimer = setTimeout(() => {
            connect();
        }, delay);
    }

    function disconnect() {
        if (reconnectTimer) {
            clearTimeout(reconnectTimer);
            reconnectTimer = null;
        }

        if (socket) {
            socket.close(1000, "Client disconnecting");
            socket = null;
        }

        set("disconnected");
        reconnectAttempts = 0;
    }

    return { subscribe, connect, disconnect };
}

export const wsStore = createWebSocketStore();