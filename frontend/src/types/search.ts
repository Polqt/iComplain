export type SearchResult = {
    id: string;
    type: 'report' | 'notification' | 'page';
    title: string;
    description?: string;
    url: string;
    icon?: string;
    meta?: string;
}

export type SearchState = {
    query: string;
    results: SearchResult[];
    recentSearches: string[];
    isSearching: boolean;
    selectedIndex: number;
}