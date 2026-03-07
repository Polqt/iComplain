export type DashboardMetric = {
    title: string;
    value: string;
    change: string;
    subtitle: string;
    trend: string;
    is_critical?: boolean;
    is_increasing?: boolean;
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
    recent_activity?: any[];
};
