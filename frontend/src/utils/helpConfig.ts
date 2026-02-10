
import helpContentData from '../data/help-content.json' with { type: 'json' };
import adminHelpData from '../data/admin-content.json' with { type: 'json' };
import type { HelpContent } from '../types/help.ts';

/**
 * Loads help content from JSON file based on role.
 * This keeps the API simple and avoids needing a full User object.
 */
export function loadHelpContent(role: 'admin' | 'student'): HelpContent {
  switch (role) {
    case 'admin':
      return adminHelpData as HelpContent;
    case 'student':
    default:
      return helpContentData as HelpContent;
  }
}

/**
 * Filters help sections by search query
 * Searches across titles, content, questions, and answers
 */
export function filterHelpSections(
  sections: HelpContent['sections'],
): HelpContent['sections'] {

  return sections.filter((section) => {
    if (
      section.title.toLowerCase() ||
      section.content.toLowerCase()
    ) {
      return true;
    }

    return section.faqs?.some(
      (faq) =>
        faq.question.toLowerCase() ||
        faq.answer.toLowerCase()
    );
  });
}