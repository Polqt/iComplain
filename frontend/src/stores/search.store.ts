import { derived, get, writable } from "svelte/store";
import type { SearchResult, SearchState } from "../types/search.ts";
import { clearRecentSearchesStorage, loadRecentSearches, performSearch, saveRecentSearches } from "../utils/useSearch.ts";


export function createSearchStore() {
    const store = writable<SearchState>({
        query: '',
        results: [],
        recentSearches: [],
        isSearching: false,
        selectedIndex: -1
    });

    const { subscribe, set, update } = store;

    let searchTimeout: ReturnType<typeof setTimeout>;

    const selectedResult = derived(store, $state => 
        $state.results[$state.selectedIndex] || null
    )

    return {
        subscribe,

        setQuery: (query: string) => {
            update(state => ({ ...state, query, selectedIndex: -1 }));
        },

        search: async (query: string) => {
            clearTimeout(searchTimeout);

            if (!query.trim()) {
                update(state => ({ ...state, query: '', results: [], isSearching: false}));
                return;
            }

            update(state => ({ ...state, query, isSearching: true }));

            searchTimeout = setTimeout(async () => {
                try {
                    const results = await performSearch(query);
                    update(state => ({
                        ...state,
                        results,
                        isSearching: false,
                        selectedIndex: results.length > 0 ? 0 : -1
                    }))
                } catch (error) {
                    update(state => ({ ...state, results: [], isSearching: false }) );
                }
            }, 300);
        },

        clear: () => {
            set({
                query: '',
                results: [],
                recentSearches: get(store).recentSearches,
                isSearching: false,
                selectedIndex: -1
            })
        },

        addRecentSearch: (query: string) => {
            if (!query.trim()) return;

            update(state => {
                const recent = [query, ...state.recentSearches.filter(q => q !== query)].slice(0, 5);
                saveRecentSearches(recent);
                return { ...state, recentSearches: recent };
            })
        },

        loadRecentSearches: () => {
            const recent = loadRecentSearches();
            update(state => ({ ...state, recentSearches: recent }));
        },

        clearRecentSearches: () => {
            clearRecentSearchesStorage();
            update(state => ({ ...state, recentSearches: [] }));
        },

        selectNext: () => {
            update(state => {
                const maxIndex = state.results.length - 1;
                const nextIndex = state.selectedIndex < maxIndex ? state.selectedIndex + 1 : 0;
                return { ...state, selectedIndex: nextIndex };
            })
        },

        selectPrevious: () => {
            update(state => {
                const maxIndex = state.results.length - 1;
                const prevIndex = state.selectedIndex > 0 ? state.selectedIndex - 1 : maxIndex;
                return { ...state, selectedIndex: prevIndex };
            })
        },

        getSelectedResult: (): SearchResult | null => get(selectedResult),
    };
}

export const searchStore = createSearchStore();

export const hasResults = derived(
    searchStore,
    $search => $search.results.length > 0
)
