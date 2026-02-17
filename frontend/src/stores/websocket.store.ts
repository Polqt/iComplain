import { PUBLIC_API_URL } from "$env/static/public";
import { writable } from "svelte/store";

type WSStatus = "connected" | "disconnected" | "connecting";

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

    }

    function handleMessage() {

    }

    function scheduleReconnect() {

    }

    function disconnect() {

    }

    return { subscribe, connect, disconnect };
}

export const wsStore = createWebSocketStore();