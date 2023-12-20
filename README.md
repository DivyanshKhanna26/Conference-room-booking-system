# Conference Room Booking System

### Table of Contents

Introduction
System Overview
Features
Data Model
System Architecture




### 1. Introduction
##### Purpose

The Conference Room Booking System is a software application designed to facilitate the
efficient booking and management of conference rooms within a multi-floor building. This
system aims to provide a user-friendly experience for both administrators and users, optimize
room utilization, and enforce organizational booking limits. It is implemented in Python and is
intended to be a command-line application.
##### Scope

The system will cover various aspects of conference room management, including adding floors
and rooms, registering organizations and users, booking rooms, canceling bookings, listing
available rooms, tracking monthly booking limits, and providing suggestions for future bookings.

### 2. System Overview
The system operates on an in-memory data model and does not rely on persistent storage. It
consists of the following key components:
* Administrators: Responsible for adding floors and rooms, registering organizations and
users, and managing room-related activities.
* Users: Registered within organizations and have permissions to book conference rooms.
* Organizations: Entities that register with the system and manage their users and room
bookings.
* Conference Rooms: Spaces available for booking, located on different floors with varying
capacities and features.
* Bookings: Records of room reservations, including the date, time slot, organization, user,
and room.

### 3. Features
* ###### Add Floor and Room Details
  Administrators can add new floors and rooms to the system, specifying floor numbers, room
  names, capacities, and additional details.
* ###### Register New Organization and Users
  Administrators can register new organizations, providing organization names and organization
  email. The Administrator can also register new users within the organization.
* ###### Room Booking
  Users can check and book conference rooms by entering the date for which they want to book,
  the timings for the booking and the capacity (no. of people) who will be using the conference
  room.
* ###### Cancel Booking
  Users can cancel their room bookings, provided the request is made at least 15 minutes before
  the booking start time.
* ###### List User/Organization Bookings
  Users can view their current and past bookings.
* ###### Suggestion Functionality
  Users have the option to receive suggestions for future time slots likely to be available for
  booking. The system analyzes historical booking data, room availability patterns, and user
  preferences to generate up to three potential slots.

### 4. Data Model
The data model consists of the following entities:
* ###### Floor
  Attributes: Floor Number
* ###### Room
  Attributes: Room Name, Capacity, Additional Details
  Relationships: Belongs to a Floor
* ###### Organization
  Attributes: Organization Name, Contact Information
* ###### User
  Attributes: Name, Email, Role, Permissions
  Relationships: Belongs to an Organization
* ###### Booking
  Attributes: Date, Time Slot, Organization, User, Room
  Relationships: Associated with a User, Organization, and Room

### 5. System Architecture
The system is designed using a modular architecture, where each feature is encapsulated within
its respective module or function. The key architectural components are as follows:
* ###### User Interface
  The system provides a command-line interface for user interaction.
  Input is taken through text-based menus and prompts, while output is displayed in a
structured format.
* ###### Business Logic
  The core logic of the system, including booking validation, monthly limit enforcement, and suggestion generation, is implemented in business logic modules.
  These modules are responsible for processing user requests and managing data.
