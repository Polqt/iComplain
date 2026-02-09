
import helpContentData from '../data/help-content.json' with { type: 'json' };
import adminHelpData from '../data/admin-content.json' with { type: 'json' };
import type { HelpContent } from '../types/help.ts';
import type { User } from '../types/user.ts';

/**
 * Loads help content from JSON file
 * This approach allows for:
 * - Easy content updates without code changes
 * - Potential localization (multiple JSON files for different languages)
 * - CMS integration in the future
 */
export function loadHelpContent(user: User): HelpContent {
  switch (user.role) {
    case 'admin': return adminHelpData as HelpContent;
    case 'student': return helpContentData as HelpContent;
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