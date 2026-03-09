# Test Strategy: Admin Dashboard

## Context

This test strategy is derived from the current repository because the requested planning inputs were not present under `docs/ways-of-work/plan/...`.

Source baseline:
- `docs/features/admin-features.mdx`
- `frontend/src/components/ui/admin/AdminDashboard.svelte`
- `frontend/src/components/ui/admin/ActivityFeed.svelte`
- `frontend/src/components/ui/tickets/TicketBoard.svelte`
- `frontend/src/lib/api/ticket.ts`
- `backend/apps/tickets/views.py`
- `frontend/package.json`
- `frontend/playwright.config.ts`
- `.github/workflows/django.yml`

Assumption:
- The feature under test is the staff-only admin dashboard rendered at `/dashboard` for authenticated users whose role resolves to `admin`.

## 1. Test Strategy Overview

### Testing Scope

In scope:
- Admin dashboard route selection and access control.
- Dashboard summary metrics from `GET /tickets/stats/dashboard`.
- Ticket volume chart rendering and empty-data handling.
- Recent activity feed from `GET /tickets/activity/`.
- Ticket status board rendering, expansion, and navigation to ticket detail flows.
- CSV export modal, client-side date validation, server-side export window validation, and file download behavior.
- Error handling for failed stats, activity, ticket, and export requests.

Out of scope for this feature package:
- Student dashboard behavior beyond regression smoke coverage.
- Full reports module, PDF/Excel exports, and analytics pages outside the dashboard.
- Email delivery content, websocket real-time guarantees, and admin category/location management.

### Quality Objectives

- Validate 100% of in-scope acceptance behavior for admin dashboard flows.
- Achieve greater than 80% line coverage for dashboard-specific frontend and backend code, with greater than 90% branch coverage on critical permission and date-validation paths.
- Cover 100% of identified high-risk scenarios before release.
- Hold dashboard summary API p95 response time below 2 seconds for the agreed test dataset.
- Hold CSV export completion below 5 seconds for the agreed non-production volume test dataset.
- Release with zero open critical or high severity defects tied to the dashboard.
- Release with no serious or critical accessibility violations in automated checks and with manual keyboard validation completed.

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
| --- | --- | --- | --- |
| Student or anonymous user can access admin-only dashboard data | Medium | Critical | Add backend authorization tests, route access tests, and Playwright access-control scenarios. |
| Dashboard counts or trends are incorrect because aggregation logic is wrong | Medium | High | Use fixed backend fixtures to validate counts, trend deltas, response-time calculations, and archived-ticket exclusion. |
| CSV export returns the wrong date range because of parsing, default-window, or timezone edge cases | High | High | Add boundary-value tests for missing dates, leap days, month ends, start-after-end, and timezone-adjacent dates. |
| One failed API call makes the dashboard unusable | Medium | High | Validate isolated error states for stats, activity feed, ticket board, and CSV export. |
| Performance degrades with larger ticket volume | Medium | High | Baseline query and response timing, validate export timing, and review cache usage before release. |
| Frontend regressions are missed because CI currently runs backend tests only | High | High | Add frontend check, unit, and Playwright stages to CI before release. |
| Mismatch between backend action/status data and frontend UI assumptions causes misleading display | Medium | Medium | Add integration tests for response schema and UI rendering with realistic payloads. |

### Test Approach

The approach is risk-based and follows the ISTQB test process with a layered test pyramid:

- Unit tests validate pure logic, helper functions, and component state transitions.
- Integration tests validate API contracts, permissions, serialization, and frontend data orchestration.
- End-to-end tests validate real user workflows in Playwright using admin and student accounts.
- Non-functional testing validates performance, accessibility, and security behavior for the release candidate.
- Regression testing protects the student dashboard and shared ticket flows affected by admin dashboard changes.

Priority order:
1. Staff-only authorization and data protection.
2. Dashboard metric correctness and export correctness.
3. Primary admin workflow continuity.
4. Performance, accessibility, and compatibility.

## 2. ISTQB Framework Implementation

### Test Process Activities

| ISTQB Activity | Admin Dashboard Application |
| --- | --- |
| Planning | Define scope, risks, entry/exit criteria, test data, environments, and GitHub issue backlog for the dashboard package. |
| Monitoring and Control | Track pass rate, defect leakage, blocked tests, and CI status at unit, integration, and Playwright levels. |
| Analysis | Derive test conditions from access rules, dashboard metrics, ticket states, export date rules, and failure states. |
| Design | Apply equivalence partitioning, boundary value analysis, decision tables, and state transition modeling. |
| Implementation | Build backend fixtures, frontend mocks, Playwright auth fixtures, and CI automation. |
| Execution | Run local developer checks, CI pipeline checks, release-candidate regression, and targeted exploratory sessions. |
| Completion | Publish coverage, defects, residual risk, waived items, and release recommendation. |

### Test Design Techniques Selection

#### Equivalence Partitioning

Apply to:
- User roles: admin, student, unauthenticated.
- Export date input classes: valid MM/DD/YYYY, invalid format, invalid calendar date, missing start, missing end.
- Dashboard data states: populated, empty, partial, backend failure.
- Ticket board data: no tickets, mixed-status tickets, archived tickets excluded.

Expected value:
- Minimizes redundant coverage while fully exercising role-based behavior and date validation.

#### Boundary Value Analysis

Apply to:
- Export window defaults at 29-day backward fill and explicit start/end boundaries.
- Month-end, leap-year, and same-day export dates.
- Empty arrays versus 1-item arrays for metrics, volume, and activity items.
- Pagination boundaries for activity logs and ticket lists where dashboard dependencies rely on list responses.

Expected value:
- Protects the feature against off-by-one and invalid-date defects, which are high-risk in the current implementation.

#### Decision Table Testing

Apply to:
- CSV export rules:
  - start missing / end missing
  - start valid / end valid
  - start invalid / end valid
  - start later than end
- Dashboard access rules:
  - authenticated + admin
  - authenticated + student
  - unauthenticated
- Error-state rendering:
  - stats fail
  - activity fails
  - ticket board fails
  - export fails

Expected value:
- Captures business-rule combinations clearly and prevents gaps across permission and validation logic.

#### State Transition Testing

Apply to:
- Admin dashboard load lifecycle: loading -> success or loading -> error.
- Export modal lifecycle: closed -> open -> validating -> exporting -> success or failure.
- Ticket card interaction: collapsed -> expanded -> detail navigation.
- Auth lifecycle on `/dashboard`: loading -> authenticated admin, authenticated student, or redirected unauthenticated user.

Expected value:
- Verifies correct UI behavior during asynchronous transitions and prevents broken intermediate states.

#### Experience-Based Testing

Apply to:
- Rapid repeated export clicks.
- Session expiry during dashboard usage.
- Midnight local-time usage affecting date defaults.
- Large activity payloads and long ticket titles/descriptions.
- Retry behavior after backend or network failure.

Expected value:
- Exposes defects that scripted tests often miss, especially around timing, browser behavior, and real user habits.

### Test Types Coverage Matrix

| Test Type | Objective | Scope | Primary Tools | Exit Signal |
| --- | --- | --- | --- | --- |
| Functional | Validate expected dashboard behavior and rules | Route gating, metrics, activity feed, board, export | Django tests, Vitest, Playwright | All critical functional scenarios pass |
| Non-functional | Validate performance, accessibility, security, compatibility | API timing, download timing, keyboard flow, role protection, browser behavior | Playwright, browser devtools, manual a11y audit, backend timing logs | Thresholds met and no blocking issues |
| Structural | Validate code-path coverage and architecture-sensitive logic | Permission branches, date parsing, empty/error branches, serializer contracts | Coverage reports, unit/integration suites | Coverage targets met for critical paths |
| Change-related | Prevent regressions in shared flows | Student dashboard, ticket listing, history links, auth flow | Regression suite in CI and release-candidate run | No critical regressions introduced |

## 3. ISO 25010 Quality Characteristics Assessment

| Characteristic | Priority | Dashboard-Specific Focus | Validation Approach | Exit Threshold |
| --- | --- | --- | --- | --- |
| Functional suitability | Critical | Correct metrics, export contents, route behavior, board rendering | Backend aggregation tests, frontend rendering tests, Playwright happy paths | 100% acceptance behavior validated |
| Performance efficiency | High | Dashboard summary load, activity fetch, ticket board load, CSV export timing | Timed API tests, browser timing capture, dataset-based checks | Summary API p95 < 2s, export < 5s |
| Compatibility | Medium | Browser behavior, desktop responsiveness, file download behavior | Chromium mandatory, Firefox/WebKit smoke, responsive manual check | No blocking browser-specific defects |
| Usability | High | Clear hierarchy, recoverable errors, obvious validation messages, modal behavior | UX-focused exploratory test, keyboard navigation, copy validation | No confusing/blocking UX defects |
| Reliability | High | Stable loading, retries, partial failure handling, consistent counts | Error-state tests, repeated-run checks, retry validation | No intermittent failures in release candidate suite |
| Security | Critical | Staff-only access, session-based protection, data leakage prevention | Authorization integration tests, Playwright role checks, manual session review | Zero critical/high security defects |
| Maintainability | High | Testability of helpers and components, CI visibility, low-fragility automation | Modular test design, fixtures, coverage reporting, CI expansion | Critical paths covered and reproducible |
| Portability | Medium | Local, CI, and preview deployment consistency | Local + CI test execution, environment variable validation | Same pass result in local and CI baseline |

## 4. Test Environment and Data Strategy

### Test Environment Requirements

Backend:
- Django application under `backend/`
- PostgreSQL-backed test database matching CI service setup
- Session-authenticated users for admin and student personas

Frontend:
- SvelteKit app under `frontend/`
- `vite preview` served through Playwright config on port `4173`
- Stable `PUBLIC_API_URL` pointing to the test backend

CI baseline:
- Current CI only runs backend migrations and `python manage.py test`
- Release readiness requires an added frontend job for `npm run check`, `npm run test:unit -- --run`, and `npm run test:e2e`

### Test Data Management

Required seeded test data:
- 1 admin user and 2 student users
- Tickets across `pending`, `in_progress`, `resolved`, and `closed`
- At least one archived ticket to validate exclusion rules
- Staff comments on selected tickets to compute response-time metrics
- Tickets spanning at least 60 days to verify current-week, last-month, and export-window logic
- Categories and priorities covering low, medium, and high urgency

Data strategy:
- Use synthetic non-production users and locations only.
- Keep deterministic fixture dates for trend and response-time assertions.
- Maintain reusable backend factory/fixture helpers for aggregation tests.
- Maintain lightweight frontend mock payloads for empty, success, and failure states.

### Tool Selection

Current tools already in repo:
- Backend: Django test runner via `python manage.py test`
- Frontend unit/integration: Vitest with `jsdom`
- End-to-end: Playwright
- Accessibility support: Storybook addon-a11y is installed

Recommended additions for this feature package:
- Frontend component-testing utilities for Svelte rendering assertions
- Playwright auth fixtures with reusable admin and student storage state
- Coverage reporting for frontend and backend critical paths
- Lightweight performance harness for API timing in CI or pre-release checks

### CI/CD Integration

Required pipeline stages for this feature:
1. Backend lint/check and Django tests.
2. Frontend static checks.
3. Frontend unit/integration tests.
4. Playwright dashboard regression suite.
5. Quality-gate summary artifact with coverage, pass rate, and defect count.

Artifact expectations:
- JUnit or equivalent test reports
- Coverage reports
- Playwright traces/screenshots on failure
- Exported defect and residual-risk summary for release review

## 5. Quality Gates

| Gate | Entry Criteria | Exit Criteria |
| --- | --- | --- |
| Test Design Ready | Feature scope, API contracts, and dashboard behavior understood; required personas identified | Strategy approved, test backlog created, high-risk scenarios mapped |
| Build Ready | Implementation merged behind stable API contracts; local app bootstraps successfully | Unit test scaffolding in place; fixtures and auth setup available |
| Integration Ready | Backend and frontend build against the same contract; test data seeded | Integration tests pass; no open critical contract mismatches |
| Release Candidate Ready | Unit, integration, and E2E suites executed on candidate build | Greater than 95% pass rate, zero critical/high defects, performance and a11y thresholds met |
| Release Sign-off | Defect triage complete, residual risks documented, regression run complete | QA recommendation recorded and evidence attached |

## 6. Completion Criteria

The admin dashboard feature is considered test-complete when:
- All critical and high-priority issues in `test-issues-checklist.md` are complete or explicitly waived by the tech lead.
- Automated coverage and pass-rate thresholds are met.
- Manual exploratory, accessibility, and role-based security checks are logged.
- Residual risks are documented in the QA sign-off package.
