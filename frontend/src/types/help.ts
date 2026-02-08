export type FAQItem = {
  question: string;
  answer: string;
}

export type HelpSection = {
  id: string;
  title: string;
  icon: string;
  content: string;
  faqs?: FAQItem[];
}

export type ContactInfo = {
  email: string;
  phone: string;
  phoneDisplay: string;
  emergencyPhone: string;
  emergencyPhoneDisplay: string;
}

export type QuickAction = {
  title: string;
  description: string;
  url: string;
  color: "primary" | "secondary" | "accent" | "info" | "success" | "warning" | "error";
}

export type HelpContent = {
  sections: HelpSection[];
  contact: ContactInfo;
  quickActions: QuickAction[];
}