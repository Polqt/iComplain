export type Report = {
    id: string;
    title: string;
    description: string;
    status: "not-started" | "in-research" | "on-track" | "complete";
    priority: "low" | "medium" | "high";
    assignees: string[];
    date: string;
    comments: number;
    links: number;
    attachments: string;
  }

export type Column = {
    id: string;
    title: string;
    color: string;
    dotColor: string;
    reports: Report[];
  }

export type ViewMode = "grid" | "list";