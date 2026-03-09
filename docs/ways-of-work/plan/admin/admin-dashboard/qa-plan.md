# Quality Assurance Plan: Admin Dashboard

## 1. QA Scope and Operating Model

This QA plan governs validation of the admin dashboard feature package for the current repository implementation.

Feature scope:
- Admin-only dashboard at `/dashboard`
- Dashboard summary metrics
- Activity feed
- Ticket status board
- CSV export modal and export endpoint

Current-state quality risks:
- Backend dashboard test files are present but empty.
- Frontend automated dashboard coverage is not yet implemented.
- CI validates backend tests only, so dashboard regressions can escape if frontend work changes.

QA operating principles:
- Risk-based prioritization first.
- Automated coverage for repeatable critical paths.
- Manual exploratory validation for timing, usability, and recovery behavior.
- Release gates tied to measurable evidence, not informal confidence.

## 2. Quality Gates and Checkpoints

| Phase | Entry Criteria | Validation Activities | Exit Criteria |
| --- | --- | --- | --- |
| Requirements and Test Design | Dashboard scope and source files reviewed; assumptions documented | Strategy review, risk review, backlog creation | Strategy approved; high-risk scenarios mapped to issues |
| Unit and Component Ready | Local build passes; fixtures available | Backend unit tests, frontend component/unit tests | Critical unit suites passing; no unresolved contract ambiguity |
| Integration Ready | Backend and frontend aligned on payload shape and auth rules | API integration tests, frontend composition tests | Contracts validated; no blocking integration defects |
| E2E Ready | Stable preview environment and seeded personas available | Playwright happy-path, download, and access-control tests | All critical E2E tests passing |
| Release Candidate | Full candidate build deployed to test environment | Regression, performance, security, accessibility, exploratory testing | Greater than 95% pass rate; zero open critical/high defects |
| Production Sign-off | Defect triage complete and residual risks documented | Final review and release recommendation | QA sign-off recorded with evidence links |

## 3. Entry and Exit Criteria by Test Type

### Unit and Component Testing

Entry criteria:
- Relevant dashboard code merged to a testable branch.
- Fixture and mock strategy available.
- Target modules identified.

Exit criteria:
- All dashboard unit suites pass.
- Critical branches for permissions and export-date validation are covered.
- No blocker defects remain unresolved at unit level.

### Integration Testing

Entry criteria:
- Backend endpoints reachable in test environment.
- Frontend configured against test backend.
- Test personas and seed data available.

Exit criteria:
- Admin, student, and unauthenticated contract scenarios pass.
- CSV export headers, content type, and date-rule behavior pass.
- No open critical integration mismatches remain.

### End-to-End Testing

Entry criteria:
- Auth fixtures or stable login flows are available.
- Preview environment is stable.
- Core dashboard data exists.

Exit criteria:
- Admin happy path passes.
- Download flow passes.
- Access-control scenarios pass.
- Failure artifacts are attached for any flaky test that needs triage.

### Non-Functional Testing

Entry criteria:
- Functional suites are stable.
- Candidate environment resembles release setup closely enough for timing checks.

Exit criteria:
- Performance thresholds met.
- No serious/critical accessibility findings remain.
- Security checks show no critical/high exposure issues.

## 4. Quality Metrics

Release metrics:
- Test pass rate: greater than 95% on candidate build
- Functional coverage: 100% of in-scope acceptance behavior
- High-risk scenario coverage: 100%
- Open defects at release: 0 critical, 0 high
- Code coverage: greater than 80% line coverage on dashboard-specific code
- Branch coverage: greater than 90% on critical permission and export-validation paths
- Accessibility: 0 serious or critical issues; manual keyboard path completed
- Performance: summary API p95 below 2 seconds; CSV export below 5 seconds

Process metrics:
- Test planning package completed in one documented review cycle
- Quality feedback turnaround below 2 business hours after candidate execution
- 100% of test issues include labels, estimates, dependencies, and acceptance criteria

## 5. GitHub Issue Quality Standards

Template compliance:
- Every issue must include scope, test type, ISTQB technique, acceptance criteria, labels, estimate, and dependencies.

Required field completion:
- Feature name
- Risk or business reason
- Reproducible task list
- Quality threshold or expected result
- Evidence attachment expectation

Labeling standards:

Test type labels:
- `test-strategy`
- `unit-test`
- `integration-test`
- `e2e-test`
- `performance-test`
- `security-test`
- `accessibility-test`
- `regression-test`

Quality labels:
- `quality-gate`
- `iso25010`
- `istqb-technique`
- `risk-based`
- `quality-validation`

Priority labels:
- `test-critical`
- `test-high`
- `test-medium`
- `test-low`

Component labels:
- `frontend-test`
- `backend-test`
- `api-test`
- `database-test`

Priority assignment rules:
- `test-critical`: access control, data correctness, export correctness, release-blocking regressions
- `test-high`: user-visible workflow continuity, performance, accessibility, strong regression risk
- `test-medium`: secondary states or lower-frequency UI behavior
- `test-low`: optional hardening or deferred exploratory depth

## 6. Task Breakdown and Estimation Strategy

### Implementation Task Types

Test implementation tasks:
- Backend aggregation and export rule tests
- Frontend component and integration tests
- Playwright dashboard workflow tests
- Performance and accessibility validation packs

Environment setup tasks:
- Seed fixture creation
- Playwright auth/session fixture creation
- CI workflow extension for frontend checks

Test data tasks:
- Deterministic dated ticket dataset
- Admin/student personas
- Archived-ticket and zero-data scenarios

Automation framework tasks:
- Coverage collection
- Failure artifact publishing
- Shared helpers for dashboard selectors and downloads

### Estimation Guidelines Applied

Applied estimates in this package follow the requested guidance:
- Unit test issue: 1 SP each for dashboard modules and helper clusters
- Integration test issue: 2 SP each for contract-heavy endpoint groups
- E2E issue: 3 SP each for workflow-heavy browser coverage
- Performance issue: 3 SP
- Security issue: 3 SP
- Accessibility issue: 2 SP
- Infrastructure enablement issue: 3 SP

Estimate review process:
- Backend owner validates backend test complexity.
- Frontend owner validates component and Playwright effort.
- Tech lead signs off on cross-cutting work and risk buffers.

## 7. Dependency Validation and Management

Blocking dependency checks:
- No circular dependencies between infrastructure, unit, integration, and E2E issues.
- API-contract issues must complete before Playwright coverage is considered stable.
- Release-candidate regression cannot begin until critical E2E paths are green.

Known dependency risks:
- Frontend tests may be blocked if auth/session setup is unstable.
- Performance testing may be misleading if test data volume is not standardized.
- Accessibility findings may require design changes late if component structure is not validated early.

Mitigation strategy:
- Complete `TST-INF-001` first.
- Reuse shared fixtures across backend, frontend, and Playwright suites.
- Run accessibility checks before final regression, not after sign-off.
- Use mocked frontend integration tests when environment instability blocks full E2E coverage, but do not waive critical Playwright checks without lead approval.

## 8. Assignment Strategy

Skill-based assignment:
- Backend-focused engineer owns aggregation, export, and authorization tests.
- Frontend-focused engineer owns component tests, page composition, and Playwright selectors.
- QA owner or test lead owns cross-feature regression, exploratory sessions, and final evidence package.

Capacity planning:
- Parallelize backend and frontend unit work after infrastructure setup.
- Keep one reviewer shared across backend and frontend issues to catch contract drift early.

Knowledge transfer:
- Pair the Playwright author with the frontend owner for selector stability.
- Pair the backend test author with the feature owner for metric business-rule review.

Cross-training:
- Use the dashboard package to establish reusable patterns for future admin feature testing.

## 9. Escalation Procedures

Escalate immediately when:
- Any critical security, authorization, or data-integrity defect is found.
- CI cannot execute required dashboard suites for more than one working day.
- Performance thresholds are missed by more than 20%.
- Accessibility blockers prevent keyboard completion of the export workflow.

Escalation path:
1. Test owner logs the defect or blocker with evidence.
2. Feature owner triages severity within the same working session.
3. Tech lead decides whether to block merge, apply a waiver, or split scope.
4. Release owner records the final disposition in the quality gate review.

Waiver policy:
- No waiver allowed for critical authorization or data-leakage defects.
- High-severity waivers require explicit tech lead approval and a dated follow-up issue.

## 10. Evidence, Reporting, and Completion

Required evidence:
- Test run summary with pass/fail counts
- Coverage output for dashboard-specific code
- Playwright traces/screenshots for failed E2E tests
- Accessibility findings and manual keyboard notes
- Performance timing notes and dataset description
- Defect log and residual-risk summary

Completion criteria:
- All critical and high-priority issues from the checklist are complete or formally waived.
- Release metrics are met.
- Quality gate review is recorded.
- Remaining risks are visible and accepted by the release owner.
