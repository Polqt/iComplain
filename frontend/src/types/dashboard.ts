export type DashboardMetric = {
    title: string;
    value: string;
    change: string;
    subtitle: string;
    trend: string;
};

export type TicketVolumeDataPoint = {
    day: string;
    value: number;
};

export type DashboardStats = {
    metrics: DashboardMetric[];
    volume: TicketVolumeDataPoint[];
    status_breakdown: Record<string, number>;
    category_breakdown: Record<string, number>;
};