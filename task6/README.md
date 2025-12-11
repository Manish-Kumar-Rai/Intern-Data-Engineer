# SQL Faker Library – Task 6

## Overview

This project implements a **SQL-based fake user generator** designed for deterministic, reproducible data generation. The system is built entirely with **PostgreSQL stored procedures**, while a Python web app provides the user interface to generate batches of fake users.

It supports multiple **locales** (e.g., English/USA and German/Germany) and allows the user to specify a **seed** to reproduce the same data consistently.

---

## Database Design

* **Extensible tables** with a `locale` column:

  * `names` – first and last names with optional gender
  * `cities` – city, region/state, postal code
  * `street_names` – street names per locale
  * `street_suffixes` – street suffixes per locale
  * `eye_colors` – eye colors per locale
  * `phone_formats` – phone number formats per locale
  * `email_domains` – email domains per locale

> This design allows adding new locales or more lookup values without changing the structure of the database.

---

## Stored Procedures

### 1. `shuffle_ids(id_array BIGINT[], seed_text TEXT) RETURNS BIGINT[]`

Shuffles an array of IDs deterministically based on a seed string.
**Purpose:** To randomize selections reproducibly without real duplication.

**Arguments:**

* `id_array` – array of IDs to shuffle
* `seed_text` – string used for deterministic shuffling

**Usage Example:**

```sql
SELECT shuffle_ids(ARRAY[1,2,3,4,5], 'demo_seed');
```

**Algorithm:**

* Implements a Fisher-Yates shuffle using a pseudo-random number generator.
* Same `id_array` + `seed_text` always produces the same shuffled array.

---

### 2. `format_name(p_locale, p_seed, p_batch_idx, p_pos_in_batch)`

Generates a **full name** and gender deterministically.

**Arguments:**

* `p_locale` – locale, e.g., `en_US`
* `p_seed` – seed string for reproducibility
* `p_batch_idx` – batch index
* `p_pos_in_batch` – row position within the batch

**Returns:**

* `full_name` – generated full name
* `out_gender` – `M` or `F`

**Algorithm:**

1. Gender is chosen with `prng_uniform(seed + '|gender', pos)`.
2. First and last names are filtered by locale and gender.
3. Names are shuffled deterministically using `shuffle_ids`.
4. `pos_in_batch % array_length` ensures variation without duplication.

**Usage Example:**

```sql
SELECT * FROM format_name('en_US','demo',0,5);
```

---

### 3. `format_address(p_locale, p_seed, p_batch_idx, p_pos_in_batch)`

Generates a **complete address** including street, house number, city, postal code, and region.

**Arguments:** Same as `format_name`

**Returns:**

* `address` – street + house number
* `out_city` – city name
* `out_postal` – postal code
* `out_region` – region/state

**Algorithm:**

* Street names, suffixes, and cities are filtered per locale.
* IDs are shuffled deterministically.
* House number is generated using `prng_int_range`.
* `pos_in_batch` ensures deterministic selection of values.

**Usage Example:**

```sql
SELECT * FROM format_address('en_US','demo',0,5);
```

---

### 4. `generate_batch(p_locale, p_seed, p_batch_idx, p_batch_size)`

Generates a batch of fake users with all attributes.

**Arguments:**

* `p_locale` – locale
* `p_seed` – seed for reproducibility
* `p_batch_idx` – batch index
* `p_batch_size` – number of users to generate

**Returns:**

* `full_name`
* `gender`
* `address`
* `city`
* `postal_code`
* `region`
* `eye_color`
* `phone`
* `email`

**Algorithm:**

1. Calls `format_name` and `format_address` for each row.
2. Eye color, phone format, and email domain IDs are shuffled deterministically.
3. Row `i` picks values using `i % array_length` to reduce repetition.
4. Email is generated from lowercase `full_name` + shuffled domain.

**Usage Example:**

```sql
SELECT * FROM generate_batch('en_US','demo',0,10);
```

---

## Deterministic Randomness

* All randomness is based on **seed + batch index + row position**.
* Ensures that repeated runs with the same parameters produce identical output.
* PRNG functions used:

  * `prng_int_range(seed, counter, min, max)` → uniform integers
  * `prng_uniform(seed, counter)` → uniform float [0,1)
  * `shuffle_ids()` → deterministic shuffle

---

## Adding New Locales

* Insert new rows in lookup tables with the desired `locale`.
* No changes to stored procedures are required.

---

## Example Query

```sql
-- Generate 10 fake users in English locale with seed 'demo'
SELECT * FROM generate_batch('en_US','demo',0,10);
```

---

## Notes

* Geolocation coordinates and physical attributes (height, weight) can be added optionally using `prng_double_range` and `prng_normal`.
* Modular design allows testing each procedure independently.
* The web application interface uses these stored procedures to fetch data and display it to the user.
