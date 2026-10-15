# Authorization Matrix - Interntrack RBAC

| Role       | Endpoint / Action               | Allowed / Restricted   | Notes                                                         |
| :--------- | :------------------------------ | :--------------------- | :------------------------------------------------------------ |
| **Intern** | `POST /submissions/`            | **Allowed**            | Can create a new submission linked to their own user ID.      |
| **Intern** | `GET /submissions/`             | **Allowed (Filtered)** | Can **only** view their own submissions (server-side filter). |
| **Intern** | `PATCH /submissions/{id}/grade` | **Forbidden (403)**    | Interns cannot grade submissions.                             |
| **Intern** | `PATCH /admin/users/{id}/role`  | **Forbidden (403)**    | Interns cannot modify user roles.                             |
| **Mentor** | `GET /submissions/`             | **Allowed (All)**      | Can view all submissions across all interns.                  |
| **Mentor** | `PATCH /submissions/{id}/grade` | **Allowed**            | Can grade submissions and add feedback.                       |
| **Mentor** | `PATCH /admin/users/{id}/role`  | **Forbidden (403)**    | Mentors cannot change user roles.                             |
| **Admin**  | `GET /submissions/`             | **Allowed (All)**      | Can view all system submissions.                              |
| **Admin**  | `PATCH /admin/users/{id}/role`  | **Allowed**            | Can update any user's role (`intern`, `mentor`, `admin`).     |
