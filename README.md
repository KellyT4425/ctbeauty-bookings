![Hero Image](static/images/CT-logo.jpg)
# **CT Beauty: Salon Appointments Made Simple**
[**Check it OUT!!!**](https://ct-beauty-bookings-34c60b5072dd.herokuapp.com/)

[**Github Repo**](https://github.com/KellyT4425/ctbeauty-bookings)

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
| **Authentication**  | django-allauth                                     | Username or email login, templates |
| **Forms (server)**  | django-crispy-forms, crispy-bootstrap5             | Clean Bootstrap 5 form rendering |
| **Frontend (client)** | Bootstrap 5, custom CSS, minimal JS               | Responsive UI, brand color `#CF9274` |
| **Database**        | PostgreSQL, `dj-database-url`                      | DB config via environment variables |
| **Static files**    | WhiteNoise                                         | Compressed static serving in prod |
| **Security**        | django-axes                                        | Brute-force protection |
| **Env/Config**      | python-dotenv                                      | Load `.env` in development |
| **Quality/Tooling** | djLint, Conventional Commits                       | Template formatting & commit convention |

## **User Stories**
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

## **Entity Relationship Diagram (ERD)**

![CT Beauty ERD](static/images/ERD-Models.jpg)

## **Entities**

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

## **Design**

## **Accessibility**

## **Testing**


## **Deployment** 🚀
[Deployed Site Link........](https://ct-beauty-bookings-34c60b5072dd.herokuapp.com/)

The project was deployed to Heroku using the following steps:

1. Sign in to Heroku and access the dashboard.
2. In the top right corner, click the **"New"** dropdown menu and then click **"Create new app"**.
3. Choose a name for your app, then change your region accordingly.
4. Click **"Create app"**.
5. On the next page that loads after clicking **"Create app"**, click **"Settings"** in the top navigation bar.
6. Click on **"Reveal Config Vars"**.
7. Add a new Config Var: type **'PORT'** in the **'KEY'** section, and type **'8000'** into the **'VALUE'** section, then click **"Add"**.
8. Next, scroll down to the **"Buildpack"** section and click **"Add buildpack"** they must be in order <em>heroku/python</em> then <em>heroku/nodejs</em> after.
9. In the top navigation bar, click the **"Deploy"** tab.
10. In the **"Deployment Method"** section, click on GitHub to connect to your GitHub account.
11. After logging into your GitHub account, search for your GitHub repository name (for this project, it was **"slot-royale"**).
12. Click on the repository once found to connect it.
13. Scroll down to the section **"Automatic Deploys"** and click on the **"Enable Automatic Deploys"** button
Then underneath, make sure the branch for the project is **"main"** and click on the **"Deploy"** button
Wait for Heroku to display that the app was deployed successfully.
1.  You can also choose **"manual deploy"**.

## **Credits**

### Django & Core Docs
- [Django Documentation](https://docs.djangoproject.com/en/4.2/) — general reference
- [Forms](https://docs.djangoproject.com/en/4.2/topics/forms/) — ModelForm, widgets
- [Messages Framework](https://docs.djangoproject.com/en/4.2/ref/contrib/messages/) — flash alerts
- [Sites Framework](https://docs.djangoproject.com/en/4.2/ref/contrib/sites/) — domain/protocol for email links
- [Settings Reference](https://docs.djangoproject.com/en/4.2/ref/settings/)
  - [Middleware](https://docs.djangoproject.com/en/4.2/topics/http/middleware/)
  - [Templates (DIRS, APP_DIRS, context processors)](https://docs.djangoproject.com/en/4.2/ref/templates/api/)
  - [Authentication backends](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#specifying-authentication-backends)
  - [Password validation](https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#password-validation)
  - [Password hashing](https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#password-hashing)
  - [Time zones](https://docs.djangoproject.com/en/4.2/topics/i18n/timezones/)
- Static files & production
  - [Static files (`STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`)](https://docs.djangoproject.com/en/4.2/howto/static-files/)
  - [collectstatic](https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#collectstatic)
  - [WhiteNoise](https://whitenoise.readthedocs.io/en/stable/) (compressed storage & middleware)

### Authentication (django-allauth)
- [Allauth Docs](https://docs.allauth.org/) — configuration & templates
- [Account settings](https://docs.allauth.org/en/latest/account/configuration.html)
  — `ACCOUNT_LOGIN_METHODS`, `ACCOUNT_SIGNUP_FIELDS`, `ACCOUNT_DEFAULT_HTTP_PROTOCOL`

### Forms Styling
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/) — `{{ form|crispy }}`, helpers/layouts
- [crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5) — Bootstrap 5 integration

### Email & Utilities (`utils.py`)
- [Django email overview](https://docs.djangoproject.com/en/4.2/topics/email/)
  and [EmailMultiAlternatives](https://docs.djangoproject.com/en/4.2/topics/email/#emailmessage-objects)
- [Rendering templates: `render_to_string`](https://docs.djangoproject.com/en/4.2/topics/templates/#django.template.loader.render_to_string)
- [Absolute URLs in emails: `build_absolute_uri`](https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpRequest.build_absolute_uri)
- iCalendar attachment: [RFC 5545 (iCalendar)](https://www.rfc-editor.org/rfc/rfc5545)

### Signals & App Wiring (`signals.py`)
- [Django signals](https://docs.djangoproject.com/en/4.2/topics/signals/) — `pre_save`, `post_save`, `post_delete`, `@receiver`
- [Run after DB commit: `transaction.on_commit`](https://docs.djangoproject.com/en/4.2/topics/db/transactions/#performing-actions-after-commit)
- [AppConfig.ready()](https://docs.djangoproject.com/en/4.2/ref/applications/#django.apps.AppConfig.ready)

### Email (SMTP)
- [Gmail SMTP settings](https://support.google.com/mail/answer/7126229)
- [Google App Passwords](https://support.google.com/accounts/answer/185833)

### Security / HTTPS
- [Deployment checklist (SSL, secure cookies)](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [`SECURE_PROXY_SSL_HEADER`](https://docs.djangoproject.com/en/4.2/ref/settings/#secure-proxy-ssl-header)

### Database & Environment
- [dj-database-url](https://github.com/jacobian/dj-database-url) — DB config from env
- [python-dotenv](https://saurabh-kumar.com/python-dotenv/) — load `.env` in dev

### Frontend
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/) — cards, tables, buttons, utilities
- [Font Awesome]()

### Tools & Linters
- [djLint](https://www.djlint.com/) — Django template formatter/linter
- [Lucid Chart](https://www.lucidchart.com/blog/automate-your-work-with-lucidchart) was used to create the ERD.

### Optional (used in this project)
- [django-axes](https://django-axes.readthedocs.io/) — brute-force protection
- [django-summernote](https://github.com/summernote/django-summernote) — rich text editor

### Support & Guidance
[Mentor](https://www.linkedin.com/in/hamiltondl/) Daniel Hamilton through each step in development, and on into production provided