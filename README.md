![Hero Image](static/images/CT-logo.jpg)
# **CT Beauty: Salon Appointments Made Simple**
| [➡️**View CT Beauty NOW!!**](https://ct-beauty-bookings-34c60b5072dd.herokuapp.com/)
| [➡️**Github Repo**](https://github.com/KellyT4425/ctbeauty-bookings) | ⭐

## **Project Description**

**CT Beauty** is a clean, responsive salon booking app — a **Django MVP** focused on the core experience: discover services, pick a treatment, and book a time slot with minimal friction. The UI is mobile-first (Bootstrap 5) with a calm, brand-led palette and accessible forms.

### What it does
- **Browse services** by category with clear descriptions, durations, and prices.
- **Book a slot**: choose a treatment, then select an available time.
- **Manage bookings (CRUD)**:
  - **Create** a booking
  - **Read** your upcoming bookings
  - **Update** (reschedule) by changing availability
  - **Delete** by cancelling the booking
- **Secure auth**: sign up / sign in with **django-allauth** (username or email), strong password rules, and brute-force protection via **django-axes**.

### How it works (at a glance)
1. **Services & Treatments** are defined in the database (admin supports full CRUD).
2. **Availability slots** represent bookable times; a **Booking** occupies one slot.
3. **Users** authenticate via allauth; protected views handle booking **CRUD** (reschedule = update).
4. The interface stays consistent across desktop, tablet, and mobile.

> Goal: deliver a smooth, trustworthy booking experience with clear information, minimal friction, and consistent styling across pages.

## **Tech Stack** 💻

| Layer                | Libraries / Tools                                  | Notes |
|---------------------|-----------------------------------------------------|------|
| **Backend**         | Django 4                                           | Core framework (MVP) |
| **Authentication**  | django-allauth 🔒                                    | Username or email login, templates |
| **Forms (server)**  | django-crispy-forms, crispy-bootstrap5             | Clean Bootstrap 5 form rendering |
| **Frontend (client)** | Bootstrap 5, custom CSS, minimal JS               | Responsive UI, brand color `#555350` |
| **Database**        | PostgreSQL, `dj-database-url`                      | DB config via environment variables |
| **Static files**    | WhiteNoise                                         | Compressed static serving in prod |
| **Security**        | django-axes                                        | Brute-force protection |
| **Env/Config**      | python-dotenv                                      | Load `.env` in development |
| **Quality/Tooling** | djLint, Conventional Commits                       | Template formatting & commit convention |

### Apps Overview

- **core** — Site shell and shared utilities.

  - `apps.py` (`CoreConfig`):
    - On startup, updates the Django **Site** object from env vars so
      email links and allauth URLs use the correct domain.
    - Env keys: `SITE_ID` (default 1), `SITE_DOMAIN`, `SITE_NAME`.

  - `forms.py`:
    - `CustomSignupForm` extends allauth’s signup to collect and save
      `first_name` and `last_name`.

## **User Stories** 🙋
- **Milestone: Functional Booking System**.

  **1.** As a logged-in user, I want to select a treatment, date, and time, So that I can schedule an appointment.

  **2.** As a potential customer, I want to browse the available treatments, So that I can decide which service to book.

  **3.** As a user, I want to see available dates and times, So that I can choose a suitable appointment slot.

  **4.** As a logged-in user, I want to view a list of my upcoming appointments, So that I can keep track of them.

  **5.** As a customer, I want to receive a booking success message, so that I know my booking is successful.

  **6.** As a user, I want to cancel or change my booking, So that I can manage my schedule as needed.

- **Milestone: Implementing User Registration and Login**.

  **1.** As a new customer, I want to register an account, So that I can log in and make a booking for a treatment.

  **2.** As a logged-in user, I want to log out of my account so that I can ensure my data is secure.

  **3.** As a user who forgot my password, I want to reset it using my email, So that I can regain access to my account.

  **4.** As a registered user, I want to log in to my account, so that I can access my personal dashboard and make or manage bookings.

- **Milestone: Admin Privileges & Control Panel**.

  **1.** As an admin, I want to view all upcoming bookings, So that I can prepare for upcoming appointments.

  **2.** As an admin, I want to change or cancel bookings, So that I can manage conflicts or emergencies.

  **3.** As an admin, I want to set my available working hours, So that customers can only book during those times.

### **Incomplete User Stories** ⌚

> Not all user stories planned for the final sprint were completed. The following user stories were not completed in the current sprint and have been added to the product backlog for future development:

#### Contact Form

**User Story**: As a visitor, I want to send a message via a contact form so that I can ask questions before booking.

- Planned Features:
  * Form fields for name, email, subject, and message
  * Validation to ensure all fields are completed
  * Submission stored or emailed to admin
  * User feedback (success/error messages) <br>
[Contact & Support](https://github.com/KellyT4425/ctbeauty-bookings/issues/14#issue-3146117866)

#### Session Management

**User Story**: As a registered user, I want active session management so that I remain securely logged in.

<em>Status</em>: Registration and login are functional, but session handling has been deferred.

- Planned Features:
  * Extended session handling and improved login state management. <br>
[Session Management](https://github.com/KellyT4425/ctbeauty-bookings/issues/24#issue-3362804998)

These stories remain in the product backlog and will be addressed in furture features.

## **Entity Relationship Diagram (ERD)** 🔁

![CT Beauty ERD](static/images/ERD-Models.jpg)

## **Entities** ↔️

#### Category
- Groups services (e.g., Brows, Lashes, Waxing).
- Fields: `name`, `slug`.

#### Treatment
- A bookable service that belongs to a category.
- Fields: name, description, duration (mins), price, slug.
- FK: `category` → Category.

#### Availability
- A single bookable slot on a specfic date & time.
- Fields: `date`, `start_time`, `end_time`, `duration`, `unavailable`, `is_booked`.

#### AvailabilityBlock

- Defines recurring opening hours across a date range.
- Fields: `start_date`, `end_date`, `start_time`, `end_time`.
- M2M: `days_of_week` → Weekday.
- <em>Used by code to generate many Availability rows (no direct FK to slots)</em>.

#### Weekday

- Lookup for days of the week.
- Fields: `number (0–6)`, `name`.

> Note: AvailabilityBlock + Weekday are used to create the Availability schedule. This is a conceptual “generates” link handled in code, not a database FK.

#### Booking

- A user’s appointment for a specific slot & treatment.
- Fields: `notes`, `status`, `created_at`, `updated_at`.
- One-to-one: availability → Availability (each slot can be booked once).
- FKs: `user` → User, treatment → Treatment.

#### User

- Django auth user (email/username) who makes bookings.

### Integrity Rules

- **No double-booking**: Booking ↔ Availability is one-to-one; chosen slot is set is_booked=True.

- **Future & duration-matched**: only future slots that match the treatment’s duration are offered.

- **Delete behaviour**:
  * Booking.user → CASCADE (deleting a user removes their bookings).
  * Booking.treatment, Booking.availability → PROTECT (avoid orphaned bookings).

### Typical Flow

**1.** Admin creates AvailabilityBlocks (e.g., Mon–Fri 09:00–17:00 for a month) → app generates Availability slots.

**2.** User selects a Treatment; form lists only future, duration-compatible slots.

**3.** On submit, a Booking is created and the chosen Availability is marked booked.

**4.** When rescheduling, only the availability (time) is changed; the previous slot is freed.

## **Design** ✏️
[Google Fonts](https://fonts.google.com/specimen/Permanent+Marker)<br>
![Fredericka the Great](static/images/google-fonts-main.png)<br>
![Baskervville](static/images/font-text.png)<br>
> Fredericka the Great <br>
> Baskervville <br>

This font pairing was chosen to:

- Differentiate hierarchy (decorative headers vs. clean body text).

- Reflect brand identity (luxury, creativity, and professionalism).

- Maintain accessibility, since serif fonts with high stroke contrast like Baskervville remain readable at body text sizes, while Fredericka the Great is used sparingly for emphasis.

[Favicons](https://favicon.io/) were created using the project’s CT Beauty branding to maintain a consistent identity across devices and platforms.<br>
![Favicon Generator](static/images/favicon-generator.png) <br>
**Purpose:**

- Provides a recognizable brand symbol in browser tabs, bookmarks, and on mobile devices.

- Ensures the application looks professional and polished across platforms.

- Enhances user trust and usability, making the site easy to identify.

[Colour Palette Generator](https://www.canva.com/colors/color-palette-generator/)
> The brand palette for CT Beauty consists of four main colours:

- Pearl Bush (#E3DAD2) – soft neutral background shade

- Fuscous Gray (#555350) – deep gray, ideal for text and accents

- Whiskey (#CF9274) – warm peach tone for highlights and accents

- Hemp (#8C7C78) – muted mauve-brown for secondary elements

These colours were chosen to reflect a modern, professional, and calming aesthetic while maintaining good readability and accessibility. <br>
![Colour Palette](static/images/palette-colour-theme.png)

## **Future Features** 👽
1. **Contact Form**
   - Allow visitors to send enquiries before booking, with validation and admin notification.

2. **Session Management**
   - Improved login session handling for enhanced security and smoother user experience.

3. **Email Confirmations for CRUD Actions**
   - Automated emails sent to users when they create, update, or cancel a booking.

4. **Admin Dashboard Enhancements**
   - Better overview of bookings, with filters by date, treatment type, or status.

5. **Booking Reminders**
   - Automated email or SMS reminders sent to users before their appointment.

6. **Waitlist Functionality**
   - If a slot is fully booked, users can join a waitlist and be notified if it becomes available.

7. **Reviews & Ratings**
   - After an appointment, users can leave a review and rating for treatments.

8. **Favourites / Repeat Booking**
   - Users can save favourite treatments or rebook past appointments with one click.


## **Accessibility**

[EightShapes](https://contrast-grid.eightshapes.com/)
> The EightShapes contrast grid was used as it helps to ensure our chosen colour palette provides enough contrast between text and background colours for users with visual impairments. The grid was provided all colours that the Colour Palette Generated provided based off of the sites main image. <br>
![Contrast Grid](static/images/contrast-table-grid.png)

The [WAVE](https://wave.webaim.org/) Accessibility Tool was used throughout development to test and improve the site’s accessibility. It highlights errors, contrast issues, missing alternative text, and ARIA labels directly on the rendered page. All issues raised by WAVE have been edited. <br>
![Wave](static/images/wave-example.png)

## **Validation** 🔍

[CI Python Linter](https://pep8ci.herokuapp.com/#)

> **CI Python Linter** The project was validated using the CI Python Linter, which checks code against PEP8 standards.

- **Result**: All files passed validation.

[Python Tutor](https://pythontutor.com/) was used during development to step through code execution visually. This tool provides an interactive way to see how variables change, how functions are called, and how data flows through the program line by line. It was especially helpful for debugging complex logic, understanding the order of operations, and building confidence in how Python executes code.

W3 HTML 5 [Validator](https://validator.w3.org/) checks complete on full deployed Heroku URL and indvidual site pages. `home`, `services`, `make a booking` etc...<br>
![HTML](static/images/html-validation.png)

Jigsaw W3 CSS 3  [Validator](https://jigsaw.w3.org/css-validator/) - The CSS files were tested with the W3C CSS Validator using the deployed site URL.
- **Result**: The code passed validation with the exception of vendor-prefixed properties (e.g., -webkit- and -moz-).
- **Explanation**: These are vendor-specific extensions added for cross-browser compatibility, particularly for handling animations and font smoothing on WebKit (Safari/Chrome) and Mozilla (Firefox) engines. They are not errors, but intentional additions to ensure consistent styling across browsers.
- **Decision**: These properties were retained to preserve user experience and compatibility.

> However Custom `style.css` file was run through the Jigsaw W3 Validator and came back with no errors. <br>

![CUSTOM](static/images/custom-css.png)

[JSHint](https://jshint.com/) | The JavaScript code was validated using JSHint.

> **Warnings**: JSHint flagged the use of modern ES6+ features (const, arrow functions =>, and optional chaining ?.) as only being available in later versions of ECMAScript.

 - **Resolution**: These warnings are not actual errors, but compatibility notes. The project intentionally uses ES6+ syntax for cleaner and more maintainable code.

 - **Summary**: No functional errors were found, and the script works as expected in modern browsers that support ES6+.

## **Testing**🔧
Manual tests were carried out to ensure the functionality of all main features.

- Form inputs were tested for validation and correct behavior.

- Buttons and navigation links were checked for responsiveness and expected results.

- Edge cases (empty fields, invalid data, incorrect routes) were verified.

- Browser compatibility and responsiveness were tested across different screen sizes.

A full breakdown of the complete test cases, results, and screenshots can be found in the [➡️ Tests](testing.md)

## Bugs 🪲

#### Bugs Encountered 🔨

During development, several issues were identified and resolved:

| Bug                                                   | Cause                                                                 | Fix                                                                |
| ----------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **`.env` not loading on Heroku**                      | `.env` was in `.gitignore`, so environment variables weren’t deployed | Added config vars directly in Heroku dashboard                     |
| **Heroku/Choco commands not working in Git Bash/WSL** | CLI tools installed only on Windows side, not in Bash/WSL PATH        | Used Windows CLI or updated PATH                                   |
| **Gunicorn worker boot failed**                       | Misconfiguration during deployment                                    | Reviewed Heroku logs via CLI, fixed settings until workers started |
| **Date picker not rendering**                         | Wrong widget import                                                   | Corrected widget import in form                                    |
| **Form allowed invalid dates**                        | Missing `clean()` validation                                          | Added validation to block end-date before start-date               |
| **Required fields failed silently**                   | Template missing `{{ form.errors }}`                                  | Added error rendering in template                                  |
| **404 from URL mismatch**                             | Trailing slash mismatch in `urls.py`                                  | Updated URL patterns                                               |
| **Broken templates after renaming views**             | Templates still referenced old URL names                              | Updated all references to new names                                |
| **Migration error: “add non-nullable field”**         | Field added without default or `null=True`                            | Supplied default value or set `null=True`                          |
| **Migration error: “column does not exist”**          | Model/field renamed without `RenameField`                             | Used proper migration operation                                    |


## **Remote Deployment (Heroku)** 🚀 [LIVE](https://ct-beauty-bookings-34c60b5072dd.herokuapp.com/)

The project was deployed to Heroku using the following steps:

1. **Repository prerequisites:**
- requirements.txt includes:
    - django,
    - gunicorn,
    - whitenoise,
    - dj-database-url,
    - psycopg2-binary,
    - django-allauth,
    - crispy-bootstrap5, etc.

> Procfile:
web: gunicorn ct_bookings.wsgi

- Optional: .python-version (e.g. python-3.12.5).

- Settings (summary):
  * whitenoise.middleware.WhiteNoiseMiddleware after SecurityMiddleware
  * STATIC_ROOT = BASE_DIR / "staticfiles"
  * STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
  * Database configured from DATABASE_URL via dj-database-url
  * All secrets and environment-specific values read from env vars

1. **Create the Heroku app:**
   1. Heroku Dashboard → New → Create new app → name + region.
   2. Add-ons: add Heroku Postgres (creates DATABASE_URL).
2. **Buildpacks:**
   - Add heroku/python.
   - Add heroku/nodejs only if the project runs an npm build. Otherwise skip.

3. **Config Vars (production):**

> Do not set PORT (Heroku sets it automatically).

- ALLOWED_HOSTS=ct-beauty-bookings-34c60b5072dd.herokuapp.com
- CSRF_TRUSTED_ORIGINS=https://ct-beauty-bookings-34c60b5072dd.herokuapp.com
- ACCOUNT_DEFAULT_HTTP_PROTOCOL=https
- SITE_DOMAIN=ct-beauty-bookings-34c60b5072dd.herokuapp.com
- SITE_NAME=CT Beauty
- SECRET_KEY=<long random>
- DATABASE_URL=<heroku postgres url>
- EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
- EMAIL_HOST=smtp.gmail.com
- EMAIL_HOST_USER=youremail@gmail.com
- EMAIL_HOST_PASSWORD=<gmail app password>
- EMAIL_PORT=587
- EMAIL_USE_TLS=True
- EMAIL_USE_SSL=False
- EMAIL_TIMEOUT=20

- SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
- DEBUG = False  # in production
- MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # first
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]

- STATIC_ROOT = BASE_DIR / 'staticfiles'
= STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#### if you have multiple Heroku apps:
`heroku run --app ct-beauty-bookings-34c60b5072dd python manage.py migrate`
`heroku run --app ct-beauty-bookings-34c60b5072dd python manage.py createsuperuser`

#### if your git remote is already the right app:
`heroku run python manage.py migrate`
`heroku run python manage.py createsuperuser`

5. **Connect repository and deploy:**
   1. App → Deploy tab → connect GitHub repo → select branch main.
   2. Click Enable Automatic Deploys (or use Manual deploy).
   3. Watch the build. Fix any collectstatic issues and redeploy if needed.

6. **Create a production superuser:**
    > heroku run python manage.py createsuperuser --app <your-heroku-app-name>

7. **Verify:**
   - Site: https://<your-app>.herokuapp.com/
   - Admin: https://<your-app>.herokuapp.com/admin/

8.  **Logs / troubleshooting:**
    > heroku logs --tail --app <your-heroku-app-name>

## **Credits**

### Primary Documentation
- [Django Docs:](https://docs.djangoproject.com/en/5.2/) Project setup, models, forms, templates, messages, middleware, static files, sites framework, auth backends, password validation/hashing, time zones.

- [django-allauth Docs:](https://docs.allauth.org/en/latest/) configuration, templates, custom forms, account settings (login methods, signup fields, default protocol).

- [crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) & crispy-bootstrap-5 Docs.

- [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) 5 Docs.

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event) (JS DOM: addEventListener, DOMContentLoaded, querySelector, optional chaining, defer).

- RFC 5545 (iCalendar) for email attachments.

### Python/Django Packages Used

- django, django-allauth, crispy-forms, crispy-bootstrap5

- dj-database-url, python-dotenv

- [whitenoise](https://whitenoise.readthedocs.io/en/latest/)

- [gunicorn](https://gunicorn.org/) (production WSGI server)

- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/) (PostgreSQL driver)

- (optional actually used) django-axes, django-summernote

### Frontend & Assets

- [Google Fonts:](https://fonts.google.com/) [list the exact families you used].

- Bootstrap 5 components (cards, tables, buttons, utilities).

- Favicon/icons: [Generator](https://favicon.io/).

- Colour palette: [Canva Generator](https://www.canva.com/colors/color-palette-generator/).

### Validation & Testing

- W3C [HTML Validator](https://validator.w3.org/), W3C [CSS](https://jigsaw.w3.org/css-validator/) Jigsaw.

- [JSHint](https://jshint.com/) (ES6+ audit notes).

- [djLint](https://djlint.com/) (Django template formatting).

- AutoPEP8 / [CI Python Linter](https://pep8ci.herokuapp.com/).

- [Lighthouse audits](testing.md) (Performance, Accessibility, Best Practices, SEO).

- [WAVE](https://wave.webaim.org/) accessibility checks.

- Manual testing: see [TESTING.md](testing.md).

### DevOps & Deployment

- [Heroku](https://id.heroku.com/login) (platform, release phase), Heroku CLI.

- WhiteNoise static file serving.

- Gmail App Passwords for email (dev), Django email utilities (EmailMultiAlternatives, render_to_string, build_absolute_uri).

### Learning References

- [Stack Overflow](https://stackoverflow.com/questions) threads consulted (null/undefined DOM access and defensive event handling).

- freeCodeCamp / CSS-Tricks guides on DOM safety and conditional handlers.

### Attribution & Licenses

- Fonts and icons licensed per their providers.

- Any third-party images/screenshots credited where used in README/Testing.

### Support & Guidance

- Mentor [Daniel Hamilton](https://www.linkedin.com/in/hamiltondl/) throughout development and into production has been so supportive and knowledgeable. Each session provided guidance that was vital to the overall completion of this project.
- CI Peer [Kristian Cross](https://www.linkedin.com/in/kristian-cross-4976622b7/) provided guidance and support, given me insight into aspects of Django and the flow of models.
- CI Tutoring Assistance and Student Care.