# Test Issues Checklist: Admin Dashboard

## Context

This backlog converts the admin dashboard test strategy into GitHub-ready work items. It is based on the existing dashboard implementation and current testing gaps in the repository.

Current baseline gaps:
- `backend/apps/tickets/tests/*.py` exist but are empty.
- Frontend end-to-end coverage is currently a single demo smoke test.
- CI only runs backend migrations and `python manage.py test`.

## Coverage Targets and Metrics

- Code coverage: greater than 80% line coverage for dashboard-specific code; greater than 90% branch coverage for permission, export-date, and error-state paths.
- Functional coverage: 100% of in-scope dashboard acceptance behavior.
- Risk coverage: 100% of high-risk scenarios from the strategy.
- Automation coverage: greater than 90% of repeatable dashboard regression checks.
- Accessibility coverage: zero serious/critical automated findings plus manual keyboard validation.
- Performance coverage: dashboard summary API p95 below 2 seconds and CSV export below 5 seconds on agreed test data volume.

## Dependency Summary

Implementation dependencies:
- Stable backend responses from `/tickets/stats/dashboard`, `/tickets/activity/`, `/tickets/`, and `/tickets/stats/dashboard/export-csv`
- Stable auth response from `/user/profile`

Environment dependencies:
- PostgreSQL-backed backend test database
- Previewable frontend application for Playwright
- Download-capable Playwright environment for CSV validation

Tool dependencies:
- Django test runner
- Vitest configuration
- Playwright with reusable auth fixtures
- Coverage reporting and CI report publishing

Cross-team dependencies:
- Frontend and backend agreement on action labels, metric ordering, and error payload format
- Delivery owner approval for performance thresholds and browser support scope

## Issue Inventory

| ID | Issue | Type | Priority | Estimate | Labels | Depends On |
| --- | --- | --- | --- | --- | --- | --- |
| TST-001 | Test Strategy: Admin Dashboard | Strategy | Critical | 3 SP | `test-strategy`, `istqb`, `iso25010`, `quality-gates` | None |
| TST-INF-001 | QA Infrastructure: Dashboard fixtures and CI enablement | Infrastructure | High | 3 SP | `quality-gate`, `frontend-test`, `backend-test`, `risk-based` | None |
| TST-UT-001 | Backend unit tests for dashboard statistics aggregation | Unit | Critical | 1 SP | `unit-test`, `backend-test`, `api-test`, `test-critical` | TST-INF-001 |
| TST-UT-002 | Backend unit tests for export window and CSV formatting | Unit | Critical | 1 SP | `unit-test`, `backend-test`, `api-test`, `test-critical` | TST-INF-001 |
| TST-UT-003 | Frontend unit tests for AdminDashboard export validation and UI state | Unit | High | 1 SP | `unit-test`, `frontend-test`, `test-high` | TST-INF-001 |
| TST-UT-004 | Frontend unit tests for ActivityFeed states and visual emphasis | Unit | Medium | 1 SP | `unit-test`, `frontend-test`, `test-medium` | TST-INF-001 |
| TST-UT-005 | Frontend unit tests for TicketBoard rendering and navigation | Unit | High | 1 SP | `unit-test`, `frontend-test`, `test-high` | TST-INF-001 |
| TST-IT-001 | Integration tests for dashboard authorization and API contracts | Integration | Critical | 2 SP | `integration-test`, `backend-test`, `api-test`, `test-critical` | TST-UT-001 |
| TST-IT-002 | Integration tests for CSV export endpoint behavior | Integration | Critical | 2 SP | `integration-test`, `backend-test`, `api-test`, `test-critical` | TST-UT-002 |
| TST-IT-003 | Frontend integration tests for dashboard composition with mocked APIs | Integration | High | 2 SP | `integration-test`, `frontend-test`, `test-high` | TST-UT-003, TST-UT-004, TST-UT-005 |
| TST-E2E-001 | Playwright tests for admin dashboard happy path | E2E | Critical | 3 SP | `playwright`, `e2e-test`, `frontend-test`, `quality-validation`, `test-critical` | TST-INF-001, TST-IT-001 |
| TST-E2E-002 | Playwright tests for CSV export validation and download | E2E | High | 3 SP | `playwright`, `e2e-test`, `frontend-test`, `quality-validation`, `test-high` | TST-INF-001, TST-IT-002 |
| TST-E2E-003 | Playwright tests for access control and session behavior | E2E | Critical | 3 SP | `playwright`, `e2e-test`, `security-test`, `test-critical` | TST-INF-001, TST-IT-001 |
| TST-PERF-001 | Performance validation for dashboard load and export | Performance | High | 3 SP | `performance-test`, `iso25010`, `test-high` | TST-IT-001, TST-IT-002 |
| TST-SEC-001 | Security validation for role protection and data exposure | Security | Critical | 3 SP | `security-test`, `iso25010`, `risk-based`, `test-critical` | TST-IT-001, TST-E2E-003 |
| TST-A11Y-001 | Accessibility validation for dashboard and export modal | Accessibility | High | 2 SP | `accessibility-test`, `iso25010`, `frontend-test`, `test-high` | TST-IT-003 |
| TST-REG-001 | Regression suite for shared dashboard, auth, and ticket flows | Regression | High | 2 SP | `regression-test`, `change-related`, `test-high` | TST-E2E-001, TST-E2E-002, TST-E2E-003 |

## Issue Details

### TST-001 - Test Strategy: Admin Dashboard

Labels:
- `test-strategy`
- `istqb`
- `iso25010`
- `quality-gates`

Checklist:
- [ ] Finalize scope, assumptions, and out-of-scope items.
- [ ] Confirm risk register and mitigation owners.
- [ ] Define quality gates and measurable thresholds.
- [ ] Publish issue backlog and dependency order.

Acceptance:
- [ ] Strategy approved by feature owner or tech lead.
- [ ] High-risk scenarios mapped to concrete tests.
- [ ] Test evidence expectations documented.

### TST-INF-001 - QA Infrastructure: Dashboard fixtures and CI enablement

Labels:
- `quality-gate`
- `frontend-test`
- `backend-test`
- `risk-based`

Checklist:
- [ ] Create reusable backend fixtures/factories for admin, student, and dated ticket scenarios.
- [ ] Add Playwright auth fixture or storage state for admin and student personas.
- [ ] Add frontend CI stages for `npm run check`, `npm run test:unit -- --run`, and `npm run test:e2e`.
- [ ] Publish coverage and Playwright failure artifacts in CI.

Acceptance:
- [ ] Tests can run repeatably in local and CI environments.
- [ ] Seed data supports metric, activity, board, and export assertions.
- [ ] CI blocks merges on failing dashboard quality gates.

### TST-UT-001 - Backend unit tests for dashboard statistics aggregation

ISTQB design:
- Technique: Equivalence partitioning + boundary value analysis
- Test type: Functional + structural

Labels:
- `unit-test`
- `backend-test`
- `api-test`
- `test-critical`

Checklist:
- [ ] Validate status counts for mixed-status tickets.
- [ ] Validate archived tickets are excluded.
- [ ] Validate response-time calculation from first staff comment.
- [ ] Validate trend text and direction for pending, resolved, and response-time metrics.
- [ ] Validate 7-day volume output for zero and non-zero days.

Acceptance:
- [ ] Fixed fixtures produce stable metric expectations.
- [ ] Critical branches in `_calculate_dashboard_stats()` are covered.

### TST-UT-002 - Backend unit tests for export window and CSV formatting

ISTQB design:
- Technique: Boundary value analysis + decision table testing
- Test type: Functional + structural

Labels:
- `unit-test`
- `backend-test`
- `api-test`
- `test-critical`

Checklist:
- [ ] Validate default 30-day window when both dates are absent.
- [ ] Validate auto-filled start when only end is provided.
- [ ] Validate auto-filled end when only start is provided.
- [ ] Validate invalid ISO date handling and start-after-end rejection.
- [ ] Validate CSV header order and exported row content.

Acceptance:
- [ ] All date-rule combinations are asserted.
- [ ] CSV output includes the expected filename and fields.

### TST-UT-003 - Frontend unit tests for AdminDashboard export validation and UI state

ISTQB design:
- Technique: Boundary value analysis + state transition testing
- Test type: Functional

Labels:
- `unit-test`
- `frontend-test`
- `test-high`

Checklist:
- [ ] Validate `MM/DD/YYYY` parsing for valid and invalid inputs.
- [ ] Validate start-date later-than-end-date error state.
- [ ] Validate modal open/close behavior.
- [ ] Validate exporting state disables conflicting actions.
- [ ] Validate stats load success and failure rendering.

Acceptance:
- [ ] Export validation messages match expected behavior.
- [ ] Loading, success, and error states render deterministically.

### TST-UT-004 - Frontend unit tests for ActivityFeed states and visual emphasis

ISTQB design:
- Technique: Equivalence partitioning + experience-based testing
- Test type: Functional

Labels:
- `unit-test`
- `frontend-test`
- `test-medium`

Checklist:
- [ ] Validate loading, empty, success, and error states.
- [ ] Validate recent activity highlighting for actions inside the 24-hour window.
- [ ] Validate fallback display for missing performer name.
- [ ] Validate history navigation affordance.

Acceptance:
- [ ] UI handles realistic activity payloads and sparse payloads cleanly.

### TST-UT-005 - Frontend unit tests for TicketBoard rendering and navigation

ISTQB design:
- Technique: Equivalence partitioning + state transition testing
- Test type: Functional

Labels:
- `unit-test`
- `frontend-test`
- `test-high`

Checklist:
- [ ] Validate empty-state rendering when there are no tickets.
- [ ] Validate column grouping by status.
- [ ] Validate expand/collapse behavior for a ticket card.
- [ ] Validate admin navigation target uses `/tickets?ticket={ticket_number}`.
- [ ] Validate student fallback navigation is unchanged in regression scenarios.

Acceptance:
- [ ] Mixed-status fixtures render in the expected columns.
- [ ] Shared navigation logic does not regress student behavior.

### TST-IT-001 - Integration tests for dashboard authorization and API contracts

ISTQB design:
- Technique: Decision table testing
- Test type: Functional + change-related

Labels:
- `integration-test`
- `backend-test`
- `api-test`
- `test-critical`

Checklist:
- [ ] Validate admin receives `200` and schema-compliant dashboard payload.
- [ ] Validate student receives `403`.
- [ ] Validate unauthenticated request is rejected.
- [ ] Validate field names and metric ordering expected by frontend consumers.

Acceptance:
- [ ] Contract assertions prevent silent backend/frontend drift.
- [ ] Role protection is enforced at API level.

### TST-IT-002 - Integration tests for CSV export endpoint behavior

ISTQB design:
- Technique: Decision table testing + boundary value analysis
- Test type: Functional + change-related

Labels:
- `integration-test`
- `backend-test`
- `api-test`
- `test-critical`

Checklist:
- [ ] Validate successful admin export with explicit range.
- [ ] Validate successful admin export with default range.
- [ ] Validate `400` response for invalid dates and reversed dates.
- [ ] Validate `403` response for non-admin access.
- [ ] Validate `Content-Disposition` and `text/csv` response headers.

Acceptance:
- [ ] Endpoint returns correct authorization and download semantics.
- [ ] Export window rules are fully covered.

### TST-IT-003 - Frontend integration tests for dashboard composition with mocked APIs

ISTQB design:
- Technique: State transition testing
- Test type: Functional + change-related

Labels:
- `integration-test`
- `frontend-test`
- `test-high`

Checklist:
- [ ] Validate dashboard page renders stats, activity feed, and ticket board together.
- [ ] Validate partial failures do not mask unrelated successful sections where intended.
- [ ] Validate retry affordances and visible error messaging.
- [ ] Validate store-backed ticket board rendering with dashboard shell.

Acceptance:
- [ ] Mocked API responses produce deterministic dashboard composition behavior.

### TST-E2E-001 - Playwright tests for admin dashboard happy path

Labels:
- `playwright`
- `e2e-test`
- `frontend-test`
- `quality-validation`
- `test-critical`

Checklist:
- [ ] Log in as admin and load `/dashboard`.
- [ ] Verify key metrics are visible.
- [ ] Verify activity feed content is visible.
- [ ] Verify ticket board loads and allows card expansion.
- [ ] Verify navigation to ticket details from the board.

Acceptance:
- [ ] Happy path passes in Chromium.
- [ ] Trace artifacts are available on failure.

### TST-E2E-002 - Playwright tests for CSV export validation and download

Labels:
- `playwright`
- `e2e-test`
- `frontend-test`
- `quality-validation`
- `test-high`

Checklist:
- [ ] Validate invalid date format shows user-facing error.
- [ ] Validate reversed date range is blocked.
- [ ] Validate successful export triggers a download with expected filename pattern.
- [ ] Validate modal closes after successful export.
- [ ] Validate export button is disabled while request is in progress.

Acceptance:
- [ ] Browser download behavior is verified end-to-end.

### TST-E2E-003 - Playwright tests for access control and session behavior

Labels:
- `playwright`
- `e2e-test`
- `security-test`
- `test-critical`

Checklist:
- [ ] Validate unauthenticated user is redirected away from `/dashboard`.
- [ ] Validate student account does not receive admin dashboard content.
- [ ] Validate admin account receives admin dashboard content.
- [ ] Validate session-loss behavior produces a recoverable redirect or denial.

Acceptance:
- [ ] End-user role gating matches backend authorization intent.

### TST-PERF-001 - Performance validation for dashboard load and export

Labels:
- `performance-test`
- `iso25010`
- `test-high`

Checklist:
- [ ] Measure dashboard summary API time against agreed fixture volume.
- [ ] Measure activity feed and ticket board dependent loads.
- [ ] Measure CSV export completion time for agreed export dataset.
- [ ] Capture slow-query or repeated-query findings for the backend owner.

Acceptance:
- [ ] Summary API p95 remains below 2 seconds.
- [ ] Export completes below 5 seconds.

### TST-SEC-001 - Security validation for role protection and data exposure

Labels:
- `security-test`
- `iso25010`
- `risk-based`
- `test-critical`

Checklist:
- [ ] Validate staff-only authorization on dashboard stats and export endpoints.
- [ ] Validate student users cannot obtain admin data through direct API calls.
- [ ] Validate dashboard does not render sensitive student/admin data beyond intended fields.
- [ ] Validate session-authenticated requests behave correctly after logout.

Acceptance:
- [ ] Zero critical or high severity security findings remain open.

### TST-A11Y-001 - Accessibility validation for dashboard and export modal

Labels:
- `accessibility-test`
- `iso25010`
- `frontend-test`
- `test-high`

Checklist:
- [ ] Validate keyboard access to export button, modal controls, and board interactions.
- [ ] Validate visible labels and button names.
- [ ] Validate focus order and focus return when modal closes.
- [ ] Validate color-contrast hotspots for trend indicators and status emphasis.

Acceptance:
- [ ] No serious or critical accessibility issues remain open.
- [ ] Manual keyboard smoke test is documented.

### TST-REG-001 - Regression suite for shared dashboard, auth, and ticket flows

ISTQB design:
- Technique: Experience-based testing
- Test type: Change-related

Labels:
- `regression-test`
- `change-related`
- `test-high`

Checklist:
- [ ] Re-run student dashboard smoke tests.
- [ ] Re-run sign-in and sign-out smoke tests.
- [ ] Re-run ticket detail navigation from dashboard board.
- [ ] Re-run history page entry from activity feed link.

Acceptance:
- [ ] No dashboard-related change breaks shared user flows.

## Sequencing and Critical Path

Recommended execution order:
1. TST-001
2. TST-INF-001
3. TST-UT-001 through TST-UT-005
4. TST-IT-001 through TST-IT-003
5. TST-E2E-001 through TST-E2E-003
6. TST-PERF-001, TST-SEC-001, TST-A11Y-001
7. TST-REG-001

Critical path:
- TST-INF-001 -> TST-IT-001/TST-IT-002 -> TST-E2E-001/TST-E2E-003 -> TST-REG-001

Parallelizable work:
- Frontend unit issues can proceed in parallel with backend unit issues after infrastructure setup.
- Accessibility and performance work can start once integration stability is reached.
