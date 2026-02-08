import type { SearchResult } from "../types/search.ts";

export async function performSearch(query: string): Promise<SearchResult[]> {
    // TODO: Replace with actual API call
    
    await new Promise(resolve => setTimeout(resolve, 300)); // Simulate network delay

    const mockResults: SearchResult[] = [
        {
        id: '1',
        type: 'report',
        title: 'Broken AC Unit in Room 301',
        description: 'Air conditioning not working properly',
        url: '/student/reports/1',
        icon: 'mdi:file-document-outline',
        meta: 'In Progress'
        },
        {
        id: '2',
        type: 'report',
        title: 'Leaking Faucet in Restroom',
        description: 'Water dripping from sink',
        url: '/student/reports/2',
        icon: 'mdi:file-document-outline',
        meta: 'Pending'
        },
        {
        id: '3',
        type: 'notification',
        title: 'Report Update',
        description: 'Your report has been reviewed',
        url: '/student/notifications',
        icon: 'mdi:bell-outline',
        meta: '2 hours ago'
        },
        {
        id: '4',
        type: 'page',
        title: 'Dashboard',
        description: 'View your reports overview',
        url: '/student/dashboard',
        icon: 'mdi:view-dashboard-outline'
        }
    ];

    // Filter results based on query
    const lowerQuery = query.toLowerCase();
    return mockResults.filter(result => 
        result.title.toLowerCase().includes(lowerQuery) ||
        result.description?.toLowerCase().includes(lowerQuery)
    );
}

export function loadRecentSearches(): string[] {
    if (typeof window === 'undefined') return [];

    try {
        const stored = localStorage.getItem('recentSearches');
        return stored ? JSON.parse(stored) : [];
    } catch (error) {
        return [];
    }
}

export function saveRecentSearches(searches: string[]): void {
    if (typeof window === 'undefined') return;

    try {
        localStorage.setItem('recentSearches', JSON.stringify(searches));
    } catch (error) {
        console.error('Failed to save recent searches:', error);
    }
}

export function clearRecentSearchesStorage() {
    localStorage.removeItem('recentSearches');
}
