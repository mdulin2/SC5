# CHANGES
## RosarioSIS Student Information System

Changes in 10.5
---------------
- JS responsive add minWidth & minHeight options to inline colorBox in jquery-colorbox.js & warehouse.js
- Trim white spaces for Contact name & Address fields in RegistrationSave.fnc.php & Address.inc.php
- Save Student Files fields, upload files in RegistrationSave.fnc.php
- CSS Do not break text inside button in stylesheet.css
- CSS responsive raise max-width for mobile & vertical tablet from 736 to 874px in zresponsive.css, rtl.css & colors.css
- HTML fix responsive table & weekdays in Calendars.php
- CSS responsive reduce select max-width from 440 to 340px in stylesheet.css & zresponsive.css

Changes in 10.4.4
-----------------
- Fix AllowUse() & AllowEdit() for User Info when on Student Info in AllowEdit.fnc.php
- CSS fix Calendar header days word-break in zresponsive.css
- CSS style time input in stylesheet.css & colors.css
- CSS remove padding for LO_SORT arrow in zresponsive.css
- HTML fix responsive / stackable table for Course Periods in Courses.php

Changes in 10.4.3
-----------------
- MySQL always use InnoDB (default), avoid MyISAM in InstallDatabase.php, Modules.inc.php, Plugins.inc.php & rosariosis_mysql.sql

Changes in 10.4.2
-----------------
- Fix SQL error null value in column "amount" in Salaries.php
- Fix Total row calculation, reset for each student in ReportCards.fnc.php & Transcripts.fnc.php, thanks to @fatahou

Changes in 10.4.1
-----------------
- JS fix regression since 9.0 & DOMPurify, open links in new window in warehouse.js
- Add Database Type and Version, add PHP version to FirstLoginPoll() in FirstLogin.fnc.php
- Fix typos in INSTALL.md & INSTALL_fr.md

Changes in 10.4
---------------
- Modcat is addon module, set custom module icon in Profiles.php & Exceptions.php
- SQL performance: use NOT EXISTS instead of NOT IN + LIMIT 1000 in Portal.php
- Add student name to Student's Absences and Grades delete prompt in MassDrops.php
- Fix display only first letter of attendance code in AttendanceSummary.php
- Remove "Minimum assignment points for letter grade" config option in Grades/Configuration.php & StudentGrades.php
- Truncate Assignment title to 36 chars in StudentGrades.php & Grades.php
- CSS date capitalize first letter only in stylesheet.css
- Add optional $id param to FilesUploadUpdate() in FileUpload.fnc.php
- JS Only show laoding spinner if file input has selected files in warehouse.js
- Add File Attached Input for existing Fees/Payments in StudentFees.php, StudentPayments.php & Student_Billing/functions.inc.php
- Add File Attached Input for existing Salaries/Staff Payments/Incomes/Expenses in Expenses.php, Incomes.php, Salaries, StaffPayments.php & Accounting/functions.inc.php
- Add-ons can add their custom Widgets in classes/core/Widgets.php & classes/core/StaffWidgets.php
- Add Widgets init action hook in Actions.php & Widgets.fnc.php
- Add Staff Widgets init action hook in Actions.php & StaffWidgets.fnc.php
- Fix SQL check student is actually enrolled in Enrollment.fnc.php
- Fix date is 1969-12-31 on Windows when PHP intl ext not activated in strftime_compat.php

Changes in 10.3.3
-----------------
- SQL ORDER BY END_DATE IS NULL DESC,END_DATE DESC (nulls first) for consistency between PostgreSQL & MySQL in User.fnc.php
- Fix PostgreSQL error column "students_join_people.address_id" must appear in the GROUP BY clause in Address.inc.php

Changes in 10.3.2
-----------------
- Fix PostgreSQL error ORDER BY "full_name" is ambiguous in DailyTransactions.php

Changes in 10.3.1
-----------------
- Fix MySQL error result as comma separated list in Export.php
- Add recommended php.ini setting session.gc_maxlifetime = 3600 in INSTALL.md, INSTALL_es.md & INSTALL_fr.md

Changes in 10.3
---------------
- Add "Cumulative Balance over school years" checkbox in StudentBalances.php
- Fix program not found when query string is URL encoded in Modules.php
- JS fix add new Period below existing Period row in Courses.php
- Add "Course Periods" checkbox in Rollover.php
- Fix MySQL error 1069 Too many keys specified; max 64 keys allowed in Fields.fnc.php & DisciplineForm.php

Changes in 10.2.3
-----------------
- Remove dead link to centresis.org in index.php
- Fix MySQL error TEXT column used in key specification without a key length in Fields.fnc.php & DisciplineForm.php
- Add ROLLOVER_ID column to User() in User.fnc.php
- Get template from last school year (rollover ID) in Template.fnc.php

Changes in 10.2.2
-----------------
- Fix PHP fatal error undefined function StudentCanEnrollNextSchoolYear() in PrintStudentInfo.php
- Set school logo with to 120px in PrintStudentInfo.php

Changes in 10.2.1
-----------------
- SQL order by Marking Period Start Date in MarkingPeriods.php, ReportCards.fnc.php, Courses.php, Schedule.php, PrintSchedules.php, MassSchedule.php, MassDrops.php & Side.php
- Maintain current month on calendar change in Calendar.php
- Maintain Calendar when closing event popup in Calendar.php
- CSS FlatSIS smaller font size for Calendar Event title in stylesheet.css
- Fix SQL error mysqli_fetch_assoc(): Argument 1 must be of type mysqli_result, null given in database.inc.php & StudentsUsersInfo.fnc.php
- When -Edit- option selected, change the auto pull-down to text field in StudentsUsersInfo.fnc.php
- HTML remove bold for "Other students associated with this address/person" in Address.inc.php
- SQL order by FULL_NAME (Display Name config option) in PortalPollNotes.fnc.php, Widget.php, GetStaffList.fnc.php, GetStuList.fnc.php, Transcripts.fnc.php, Courses.php, MassRequests.php, ScheduleReport.php & Address.inc.php
- CSS fix Report Cards PDF columns size when long comments text in ReportCards.fnc.php & stylesheet_wkhtmltopdf.css
- CSS Add .grade-minmax-wrap,.grade-minmax-min,.grade-minmax-grade & .grade-minmax-max classes & avoid breaking grades in stylesheet.css & ReportCards.fnc.php
- Fix get Min. Max. grades for students in distinct grade levels in FinalGrades.php
- Fix SQL syntax error since 10.0 in Administration.php
- CSS Do not break words inside lists in stylesheet.css
- SQL handle case when student dropped and then later re-enrolled in course in DuplicateAttendance.php
- Use DBEscapeIdentifier() for Gradebook ASSIGNMENT_SORTING in Assignments.php, GradebookBreakdown.php & Grades.php

Changes in 10.2
---------------
- Add StudentCanEnrollNextSchoolYear() & StudentEnrollNextSchoolYear() functions in Enrollment.fnc.php
- Add "Enroll student for next school year" in Enrollment.inc.php
- Translate "Enroll student for next school year" to French & Spanish in rosariosis.po
- MySQL fix character encoding when translating database in InstallDatabase.php

Changes in 10.1
---------------
- Fix MySQL 5.6 syntax error when WHERE without FROM clause, use dual table in TakeAttendance.php, Reminders.php,  InputFinalGrades.php, Requests.php & Calendar.php
- Add dual VIEW for compatibility with MySQL 5.6 to avoid syntax error when WHERE without FROM clause in rosariosis.sql & Update.fnc.php
- Fix MySQL 5.6 syntax error in ORDER BY use report_card_comments table instead of dual in InputFinalGrades.php
- Fix SQL use cast(extract(DOW) AS int) for PostrgeSQL in Calendar.php
- Add instructions for MySQL in INSTALL.md, INSTALL_es.md & INSTALL_fr.md

Changes in 10.0
---------------
- SQL convert table names to lowercase, program wide
- Fix delete file attached in StudentFees.php
- Use DBEscapeIdentifier() for reserved 'column' keyword in plugins/Moodle/
- Avoid regression due to lowercase table names: Maintain compatibility with add-ons using rollover_after action hook & `$_REQUEST['tables']` in Rollover.php
- Use db_trans_*() functions in DeleteTransaction.fnc.php & DeleteTransactionItem.fnc.php
- Close popup if no UserSchool in session, happens on login redirect in Warehouse.php
- SQL order Grade Levels in StudentBreakdown.php
- Remove semicolon before "With" & "On" values in PrintRequests.php & unfilledRequests.inc.php
- HTML Link is selected: bold in ScheduleReport.php
- Display Period title if no short name set in IncompleteSchedules.php
- Fix Widget search & add Search Terms header in IncompleteSchedules.php
- Add Schedule link & photo tooltip to Student name in Scheduling/AddDrop.php
- HTML add a11y-hidden label to select in GPARankList.php & Attendance/TeacherCompletion.php
- Fix unset requested dates in MassCreateAssignments.php & Assignments.php
- Add User / Student photo tooltip in Grades/TeacherCompletion.php, GPARankList.php & EnterEligibility.php
- SQL order by Period title in TeacherCompletion.php
- Use Period's Short Name when > 10 columns in the list in TeacherCompletion.php
- Add note on save in EntryTimes.php
- Fix PHP8.1 Deprecated passing null to parameter in EmailReferral.fnc.php, CategoryBreakdown.php & StudentGrades.php
- Add Total sum of balances in StaffBalances.php
- Fix French translation for "Waiver" & "Refund" in rosariosis.po
- Force title & action to lowercase in Prompts.php
- HTML use .dashboard-module-title CSS class for module titles in Profiles.php & Exceptions.php
- CSS set input label max-width on Search form in stylesheet.css
- JS new default popup size: 1200x450 in warehouse.js
- Use URLEscape() for add button link when appropriate in ListOutput.fnc.php
- JS set Calendar date to current fields date in warehouse.js & calendar-setup.js
- HTML add label to select in ActivityReport.php
- Use Currency() function instead of number_format() in TransactionsReport.php
- HTML remove line-break in Warning/Minimum columns in Reminders.php
- HTML CSS make Daily Menus calendar coherent with School Calendar in DailyMenus.php
- Shorten Referral email subject in EmailReferral.fnc.php
- Use plural wise ngettext() for "No %s were found." in FinalGrades.php, GradeBreakdown.php, ReportCardComments.php, ReportCards.php & Transcripts.php
- Force result text to lowercase for "No %s were found." in ListOutput.fnc.php, FinalGrades.php, GradeBreakdown.php, ReportCardComments.php, ReportCards.php & Transcripts.php
- Prevent admin from removing own access to User Profiles program in Profiles.php
- SQL change modname column type from text to varchar(150) to match with MySQL key index limitation in rosariosis.sql
- SQL change program column type from text to varchar(100) NOT NULL to match with MySQL index limitation in rosariosis.sql
- SQL change schools column type from text to varchar(150) to match with MySQL index limitation in rosariosis.sql
- Rename YEAR_MONTH column alias to YEAR_MONTH_DATE: reserved keyword in MySQL in Dashboard.inc.php
- SQL use DAYOFWEEK() for MySQL or cast(extract(DOW)+1 AS int) for PostrgeSQL, program wide
- SQL cast(AS UNSIGNED) for MySQL or cast(AS INT) for PostgreSQL, program wide
- SQL cast custom_fields ID AS char(10) instead of TEXT for MySQL compatibility in GetStaffList.fnc.php, GetStuList.fnc.php & Search.fnc.php
- SQL rename $field COLUMN (reserved keyword) to COLUMN_NAME for MySQL compatibility in CustomFields.fnc.php, GetStaffList.fnc.php, GetStuList.fnc.php & Search.fnc.php
- SQL remove use of nextval in rosariosis_fr.sql
- Rename $pg_dumpPath configuration variable to $DatabaseDumpPath in config.inc.sample.php, diagnostic.php & DatabaseBackup.php
- Build command for executing mysqldump in DatabaseBackup.php
- SQL to extract Unix timestamp or epoch from date in Eligibility/Student.php, StudentList.php & TeacherCompletion.php
- Install module/plugin: execute the install_mysql.sql script for MySQL in Modules.inc.php, Plugins.inc.php & modules/README.md & plugins/README.md
- Fix typo "inexistant" to "nonexistent" & update translations in Modules.inc.php, Plugins.inc.php & rosariosis.po
- HTML fix duplicated #menu-top div on update in Side.php
- JS fix #body height calculation: include bottom margin in jquery-fixedmenu.js & plugins.min.js
- Add MySQLRemoveDelimiter() remove DELIMITER $$ declarations before procedures or functions in database.inc.php, Modules.inc.php & Plugins.inc.php
- SQL ORDER BY SORT_ORDER IS NULL,SORT_ORDER (nulls last) for consistency between PostgreSQL & MySQL, program wide
- Rollback Fix PostgreSQL error invalid ORDER BY, only result column names can be used, program wide
- HTML use number input for Gradebook config options in Configuration.php
- HTML use number input for Grade points & average in ReportCardGrades.php
- SQL limit results to current school year in AddDrop.php
- SQL always use INTERVAL to add/subtract days to date for MySQL compatibility in Reminders.php, Transactions.php, ServeMenus.php, Assignments.php, StudentGrades.php, Rollover.php & Portal.php
- SQL change amount columns type from numeric to numeric(14,2) NOT NULL in rosariosis.sql & StudentFees.php
- SQL change minutes,minutes_present,points,default_points,length,count_weighted_factors,count_unweighted_factors columns type from numeric to integer in rosariosis.sql, UpdateAttendanceDaily.fnc.php, Assignments.php, MassCreateAssignments.php & Periods.php
- SQL change gp & gpa columns type from numeric to numeric(7,2) in rosariosis.sql
- SQL change sum/cum factors & credit_attempted/earned columns type from numeric to double precision in rosariosis.sql
- Add Can use modname to HACKING ATTEMPT error email in ErrorMessage.fnc.php
- Fix HACKING ATTEMPT when Grades module inactive in Portal.php & Calendar.php
- Use GetTemplate() instead of unescaping `$_REQUEST` in CreateParents.php & NotifyParents.php
- Use `$_POST` to get password instead of unescaping `$_REQUEST` in PasswordReset.php, Student.php & User.php
- Use DBGetOne() instead of unescaping `$_REQUEST` in Config.fnc.php
- Add MySQL support in database.inc.php, diagnostic.php, InstallDatabase.php & Warehouse.php
- Add $DatabaseType configuration variable in database.inc.php, diagnostic.php, InstallDatabase.php, Warehouse.php & config.inc.php
- Add $show_error parameter to db_start() in database.inc.php
- Add DBUnescapeString() function in database.inc.php, GetStuList.fnc.php, ListOutput.fnc.php, PreparePHP_SELF.fnc.php & Search.fnc.php
- PostgreSQL Date format: move query from Date.php to Warehouse.php
- Compatibility with add-ons version < 10.0, gather CONFIG (uppercase table name) values too in Configuration.php
- Fix MySQL error Table is specified twice, both as a target for 'INSERT' and as a separate source for data in CopySchool.php & Rollover.php
- Fix MySQL syntax error: no table alias in DELETE in Rollover.php
- Fix MySQL syntax error: no FROM allowed inside UPDATE, use subquery or multi-table syntax in Rollover.php
- Fix MySQL syntax error: replace CAST (NULL AS CHAR(1)) AS CHECKBOX with NULL AS CHECKBOX in AddAbsences.php, AddActivity.php, MassDrops.php, MassRequests.php, MassSchedule.php, AddUsers.php, AssignOtherInfo.php & AddStudents.php
- Add Installation tutorial for Mac in WHATS_NEW.md & INSTALL.md, INSTALL_fr.md & INSTALL_es.md
- Update tested on Ubuntu 18.04 to 20.04 in INSTALL.md, INSTALL_fr.md & INSTALL_es.md
- Fix SQL error when column already dropped in Fields.fnc.php
- SQL fix CREATE INDEX on right table in rosariosis.sql
- SQL remove unused indices for various tables in rosariosis.sql
- SQL match index with FOREIGN KEY for various tables in rosariosis.sql
- SQL ORDER BY fix issue when Transferring to another school & new start date is <= old start date in Enrollment.inc.php
- Check if student already enrolled on that date when inserting START_DATE in SaveEnrollment.fnc.php
- Add `_getAddonsSQL()` & `_configTableCheck()` functions in InstallDatabase.php
- $DatabasePort configuration variable is now optional in config.inc.sample.php, INSTALL.md, INSTALL_es.md & INSTALL_fr.md
- SQL start staff_fields ID sequence at 200000000 for coherence with custom_fields in rosariosis.sql & Fields.fnc.php
- MySQL use LONGTEXT type for textarea field in Fields.fnc.php & DisciplineForm.php
- SQL Check requested assignment belongs to teacher in Assignments.php
- CSS fix responsive when really long string with no space in stylesheet.css
- Limit `$_POST` array size to a maximum of 16MB in Warehouse.php, thanks to @ahmad0x1
- Add optional ROSARIO_POST_MAX_SIZE_LIMIT constant in Warehouse.php, INSTALL.md, INSTALL_es.md & INSTALL_fr.md
- Add MySQL database dump in rosariosis_mysql.sql
- Log "RosarioSIS HACKING ATTEMPT" into Apache error.log in HackingLog.fnc.php
- Force URL & menu reloading, always use JS to redirect in HackingLog.fnc.php
- Place currency symbol after amount for some locales in Currency.fnc.php
- SQL use timestamp type: standard & without time zone by default in rosariosis.sql
- CSS add .accounting-totals, .accounting-staff-payroll-totals, .student-billing-totals classes in Expenses.php, Incomes.php, Salaries.php, StaffPayments.php, StudentFees.php & StudentPayments.php
- SQL rename KEY (reserved keyword) to SORT_KEY for MySQL compatibility in Search.fnc.php, StudentFieldBreakdown.php, StudentBreakdown.php
- SQL use GROUP BY instead of DISCTINCT ON for MySQL compatibility in Address.inc.php & EnterEligibility.php
- SQL cast Config( 'STUDENTS_EMAIL_FIELD' ) to int when custom field in SendNotification.fnc.php, Registration.fnc.php, Moodle/getconfig.inc.php & ImportUsers.fnc.php
- Fix MySQL 5.6 error Can't specify target table for update in FROM clause in PortalPollsNotes.fnc.php, DeleteTransaction.fnc.php, DeleteTransactionItem.fnc.php, Rollover.php, CopySchool.php & AssignOtherInfo.php
- Fix MySQL syntax error: explicitly list all columns instead of wildcard in ActivityReport.php & Statements.php
- Fix MakeChooseCheckbox() remove parent link to sort column in Inputs.php & ListOutput.fnc.php
- CSS WPadmin fix menu select width in stylesheet.css
- Enrollment Start: No N/A option for new student in StudentUsersInfo.fnc.php

Changes in 9.3.2
----------------
- Fix regression since 9.2.1 fields other type than Select Multiple from Options in CategoryBreakdownTime.php

Changes in 9.3.1
----------------
- Fix regression since 2.9 Schedule multiple courses in plugins/Moodle/Scheduling/MassSchedule.php
- Fix SQL to select Periods where exists CP in TeacherCompletion.php & Administration.php
- Fix dummy day (year month date) set to 28 for February in Dashboard.inc.php
- Fix AllowEdit for Teacher in Users/includes/General_Info.inc.php
- Security: sanitize filename with no_accents() in Student.php, User.php & Schools.php
- Fix "Exclude PDF generated using the "Print" button" option for the PDF Header Footer plugin in Bottom.php

Changes in 9.3
--------------
- Handle case where Course Period Parent ID is null in Courses.php
- SQL order by Period title in Periods.php, DailySummary.php & StudentSummary.php
- SQL get Period title if no short name set in AddAbsences.php
- Use DBLastInsertID() instead of DBSeqNextID() in Moodle/includes/ImportUsers.fnc.php
- Still use DBSeqNextID() for student ID, adapt for MySQL in Student.php & Moodle/includes/ImportUsers.fnc.php
- SQL use CONCAT() instead of pipes || for MySQL compatibility, program wide
- Fix first item in the list not displayed in Accounting/includes/DailyTransactions.php
- SQL time interval for MySQL compatibility in PasswordReset.php & index.php
- SQL use CAST(X AS char(X)) instead of to_char() for MySQL compatibility in Dashboard.inc.php & Reminders.php
- SQL result as comma separated list for MySQL compatibility in Grades/includes/Dashboard.inc.php & MasterScheduleReport.php
- Use DBEscapeIdentifier() for MySQL reserved 'TIMESTAMP' keyword in ServeMenus.php & Transactions.php
- SQL add `_SQLUnixTimestamp()` to extract Unix timestamp or epoch from date in Grades.php & Schedule.php
- Add case for MySQL: get next MP ID & set AUTO_INCREMENT+1 in EditHistoryMarkingPeriods.php
- Display Name: SQL use CONCAT() instead of pipes || for MySQL compatibility in Configuration.php & GetStuList.fnc.php
- config table: update DISPLAY_NAME to use CONCAT() instead of pipes || in Update.fnc.php

Changes in 9.2.2
----------------
- Fix SQL error lastval is not yet defined when editing field in SchoolFields.php, AddressFields.php, PeopleFields.php, StudentFields.php, UserFields.php & Assignments.php

Changes in 9.2.1
----------------
- Remove use of db_seq_nextval(), use auto increment, program wide
- SQL set default nextval (auto increment) for RosarioSIS version < 5.0 on install & old add-ons in Update.fnc.php
- SQL no more cast MARKING_PERIOD_ID column as text/varchar in rosariosis.sql & InputFinalGrades.php
- PLpgSQL compact & consistent function declaration in rosariosis.sql
- Use DB transaction statements compatible with MySQL in database.inc.php
- Add DBLastInsertID() & deprecate DBSeqNextID() + db_seq_nextval() in database.inc.php
- SQL rename character varying & character data types to varchar & char in rosariosis.sql
- SQL replace use of STRPOS() with LIKE, compatible with MySQL in PortalPollNotes.fnc.php & Courses.php
- SQL fix French & Spanish translation for Create Parent Users & Notifiy Parents email templates in rosariosis_fr.sql & rosariosis_es.sql
- Use DBLastInsertID() instead of DBSeqNextID(), program wide
- SQL TRIM() both compatible with PostgreSQL and MySQL in AttendanceSummary.php & CopySchool.php
- SQL use extract() or SUBSTRING() or REPLACE() instead of to_char() for MySQL compatibility, program wide
- Fix No Address contact not properly saved for student / parent in RegistrationSave.fnc.php
- AddDBField() Change $sequence param to $field_id, adapted for use with DBLastInsertID() in Fields.fnc.php, SchoolFields.php, AddressFields.php, PeopleFields.php, StudentFields.php & UserFields.php
- Raise Frame file size limit to 5MB in HonorRoll.fnc.php
- Fix Marking Period not found in user School Year (multiple browser tabs case) in MassSchedule.php & MassDrops.php
- Fix Course not found in user School Year (multiple browser tabs case) in MassRequests.php
- HTML add label to inputs in Requests.php
- Remove help sentence. The Scheduler is not run by the Student Requests program in Help_en.php

Changes in 9.2
--------------
- Fix SQL error invalid input syntax for integer in Administration.php
- SQL student_report_card_grades table: convert MARKING_PERIOD_ID column to integer in Update.fnc.php, rosariosis.sql, EditReportCardGrades.php, FinalGrades.php & ReportCards.fnc.php

Changes in 9.1.1
----------------
- Fix PHP8.1 fatal error unsupported operand types: string / int in Assignments.php & MassCreateAssignments.php
- Fix selected Subject lost on Comment Category delete in ReportCardComments.php
- Fix Color Input was hidden in ReportCardComments.php
- Fix use Course ID in session in MassRequests.php
- Fix SQL error primary key exists on table food_service_staff_accounts in Rollover.php
- Fix SQL error foreign key exists on tables gradebook_assignments,gradebook_assignment_types,schedule_requests in Rollover.php
- Fix save State input value in Registration.fnc.php
- Fix SchoolInfo() on user School Year update in School.php

Changes in 9.1
--------------
- Fix stored XSS security issue: decode HTML entities from URL in PreparePHP_SELF.fnc.php, thanks to @domiee13
- Capitalize month when date is only month and year in Dashboard.inc.php
- Add decimal & thousands separator configuration in Help_en.php, Currency.fnc.php, Configuration.php, rosariosis.sql & rosariosis_fr.sql
- Use Currency() for Food Service Balance value in Widget.php & StaffWidget.php
- Add Class average in InputFinalGrades.php & Grades.fnc.php
- Update French & Spanish translation in rosariosis.po & help.po
- Update Default School Year to 2022 in config.inc.sample.php & rosariosis.sql

Changes in 9.0
--------------
- CSS add length to previous meals select in DailyMenus.php
- CSS FlatSIS fix calendar menu text wrapping in stylesheet.css
- Add Export list button in TransactionsReport.php
- Add Food Service icon to list in ServeMenus.php
- Add User / Student photo tooltip in ServeMenus.php, Transactions.php & TeacherCompletion.php
- HTML add horizontal ruler before each category in MakeReferral.php
- Fix SQL error when generating Schedule table with PHP8.1 in GetMP.php
- Reorder PDF list columns to match Schedule columns in PrintSchedules.php
- SQL order Schedule list by Course Title & Course Period Short Name in Schedule.php, PrintSchedules.php & Schedule.inc.php
- Fix SQL error more than one row returned by a subquery in Rollover.php
- Fix update Course Period title when Short Name contains single quote in Courses.php
- Fix PHP8.1 deprecated function parameter is null, program wide
- Fix PHP8.1 deprecated automatic conversion of false to array in StudentsUsersInfo.fnc.php
- Fix PHP8.1 deprecated automatic conversion of float to int in ImageResizeGD.php
- Add Student Photo Tip Message in AddDrop.php & StudentList.php
- Format Enrollment Start & End Date in Export.php
- Add Student name if no Contacts at address in MailingLabel.fnc.php
- Do not Export Delete column in Periods.php & GradeLevels.php
- HTML group inputs inside fieldset (tab title or program name) in Configuration.php
- Hide Comment Codes tip message if Comments unchecked for Marking Period in InputFinalGrades.php
- Add Get Student Labels Form JS (Disable unchecked fieldset) in StudentLabels.fnc.php & StudentLabels.php
- Fix PHP8.1 deprecated use PostgreSQL $db_connection global variable in database.inc.php & Grades/includes/Dashboard.inc.php
- Don't Delete Gender & Birthday Student Fields in Fields.fnc.php
- CSS set cursor for .tipmsg-label in stylesheet.css
- Add Username to Password Reset email in PasswordReset.php
- `intl` PHP extension is now required in diagnostic.php & INSTALL.md
- Fix PHP8.1 deprecated strftime() use strftime_compat() instead in Side.php, Date.php, PHPCompatibility.php, strftime_compat.php, Dashboard.inc.php & Preferences.php
- Add $course_period_id param to limit check to a single Course Period in Courses.fnc.php & Courses.php
- Add title to Contact & Address button images in Address.inc.php & GetStuList.fnc.php
- CSS select max-width 440px in stylesheet.css & zresponsive.css
- HTML add label to Points inputs to correct alignment in Grades.php
- HTML add a11y-hidden label to select in CategoryBreakdown.php, CategoryBreakdownTime.php & StudentFieldBreakdown.php
- Place Go button right after Timeframe in DailyTransactions.php, DailyTotals.php, CategoryBreakdown.php, CategoryBreakdownTime.php, StudentFieldBreakdown.php & Percent.php
- Fix French translation for "Not due" in rosariosis.po
- Move Transcript Include form checkboxes up in Transcripts.fnc.php
- Add Delete button for Submission File in StudentAssignments.fnc.php
- Fix SQL error null value in column "title" violates not-null constraint in MassCreateAssignments.php
- Reorder & rename Course Periods columns to match Schedule program in MassCreateAssignments.php
- Fix get History Grades Grade Level short name only if no Grade Level available in Transcripts.fnc.php
- Fix get Student Photo from previous year in Transcripts.fnc.php
- Fix SQL error invalid input syntax in PrintSchedules.php & TeacherCompletion.php, thanks to @scgajge12
- Filter IP, HTTP_* headers can be forged in index.php, PasswordReset.php & ErrorMessage.fnc.php
- Fix SQL error invalid input syntax for integer, program wide
- Fix PHP8.1 fatal error checkdate argument must be of type int in Calendar.php
- Fix SQL error invalid input syntax for type date in Calendar.php
- Fix SQL error duplicate key value violates unique constraint "attendance_calendar_pkey" in Calendar.php
- Fix PHP fatal error Unsupported operand types in ListOutput.php
- Add AttrEscape() function in Inputs.php
- Use AttrEscape() instead of htmlspecialchars(), program wide
- Add use of AttrEscape(), program wide
- Maintain Advanced search when editing Timeframe in Percent.php
- Fix SQL injection escape DB identifier in RegistrationSave.fnc.php, Calendar.php, MarkingPeriods.php, Courses.php, SchoolFields.php, AddressFields.php, PeopleFields.php, StudentFields.php, UserFields.php & Referrals.php
- JS update marked to v4.0.14 in assets/js/marked/ & warehouse_wkhtmltopdf.js
- JS add DOMPurify 2.3.6 in assets/js/DOMPurify/ & Gruntfile.js
- JS fix stored XSS issue related to MarkDown in warehouse.js & plugins.min.js, thanks to @intrapus
- JS remove logged in check on history back in warehouse.js & plugins.min.js
- Add CSRF token to protect unauthenticated requests in Warehouse.php & login.php
- Add CSRF token to logout URL in login.php, Warehouse.php, PasswordReset.php, Bottom.php, Student.php & User.php, thanks to @khanhchauminh
- Logout after 10 Hacking attempts within 1 minute in HackingLog.fnc.php
- Destroy session now: some clients do not follow redirection in HackingLog.fnc.php
- Add use of URLEscape(), program wide
- Use URLEscape() for img src attribute, program wide
- Sanitize / escape URL as THEME is often included for button img src attribute in User.fnc.php
- Better format for "Add another marking period" form in EditReportCardGrades.php
- Fix Improper Access Control security issue: add random string to photo file name in TipMessage.fnc.php, Transcripts.fnc.php, PrintClassPictures.php, Student.php, User.php & General_Info.inc.php, thanks to @dungtuanha
- Fix stored XSS security issue: decode HTML entities from URL in PreparePHP_SELF.fnc.php, thanks to @khanhchauminh
- Fix stored XSS security issue: remove inline JS from URL in PreparePHP_SELF.fnc.php, thanks to @intrapus & @domiee13
- Fix stored XSS security issue: add semicolon to HTML entity so it can be decoded in PreparePHP_SELF.fnc.php, thanks to @intrapus
- Accessibility: add hidden input label using .a11y-hidden class in ReportCardComments.php, StudentFields.php & Grades/TeacherCompletion.php
- Accessibility: add select label in Eligibility/TeacherCompletion.php, Student.php, StudentList.php, MassDrops.php & MassSchedule.php
- Two Lists on same page: export only first, no search in Eligibility/Student.php
- Remove photos on delete in Student.php & User.php, thank to @jo125ker
- Remove Student Assignment Submission files on delete in Assignments.php, thank to @khanhchauminh
- Add microseconds to filename format to make it harder to predict in Assignments.php & StudentAssignments.fnc.php, thanks to @khanhchauminh
- Restrict Sort Order input number range, program wide
- Restrict Price / Amount / Balance input number range, program wide, thanks to @nhienit2010
- Restrict input number step in Courses.fnc.php
- Restrict diagnostic access to logged in admin in diagnostic.php, thanks to @intrapus
- Fix SQL error value too long for type character varying(50) in Schools.php
- Add Secure RosarioSIS link in INSTALL.md
- Add Calendar days legend in Calendar.php
- CSS add .legend-square class in stylesheet.css & colors.css
- Create / Edit / Delete calendar: use button() in Calendar.php
- Update Calendars help text in Help_en.php & help.po
- Add translations for Calendar days legend in rosariosis.po
- Use json_encode() for AjaxLink() URL, program wide
- SQL skip "No Address" contacts to avoid lines with empty Address fields in Export.php
- French translation: remove capitalization & use articles in rosariosis.po, help.po & rosariosis_fr.sql
- JS Sanitize string for legal variable name in Export.php & Inputs.php
- Remove deprecated `_makeTeacher()` function in ReportCards.fnc.php
- Use multiple select input for grades list to gain space in Widget.php
- Fix regression since 5.0, allow Administration of "Lunch" attendance categories in Administration.php, AttendanceCodes.fnc.php & colors.css
- SQL set default FAILED_LOGIN_LIMIT to 30 in rosariosis.sql, thanks to @domiee13
- JS Hide Options textarea if Field not of select type in Fields.fnc.php
- Add Balance widget in StudentBalances.php
- Add Total sum of balances in StudentBalances.php
- Fix SQL error check requested UserSyear & UserSchool exists in DB in Side.php, Search.fnc.php & SaveEnrollment.fnc.php
- HTML use number input for Class Rank widget in Widget.php
- Check default if school has no default calendar in Calendar.php
- CSS do not capitalize date in stylesheet.css
- Remove unused index ON attendance_period (attendance_code) & ON student_report_card_grades (school_id) in rosariosis.sql & rosariosis_mysql.sql
- SQL VACUUM & ANALIZE are for PostgreSQL only in Scheduler.php


### Old versions CHANGES
- [CHANGES for versions 7 and 8](CHANGES_V7_8.md).
- [CHANGES for versions 5 and 6](CHANGES_V5_6.md).
- [CHANGES for versions 3 and 4](CHANGES_V3_4.md).
- [CHANGES for versions 1 and 2](CHANGES_V1_2.md).
