-- 03_generators.sql

-- Helper: Deterministic shuffle using PRNG
CREATE OR REPLACE FUNCTION shuffle_ids(id_array BIGINT[], seed_text TEXT)
RETURNS BIGINT[]
LANGUAGE plpgsql AS $$
DECLARE
    array_len INT := array_length(id_array,1);
    idx INT;
    rand_idx INT;
    tmp BIGINT;
BEGIN
    IF array_len IS NULL OR array_len = 0 THEN
        RETURN ARRAY[]::BIGINT[];
    END IF;

    FOR idx IN REVERSE array_len..2 LOOP
        rand_idx := 1 + prng_int_range(seed_text, idx, 0, idx-1);
        tmp := id_array[idx];
        id_array[idx] := id_array[rand_idx];
        id_array[rand_idx] := tmp;
    END LOOP;

    RETURN id_array;
END
$$;

-- FORMAT NAME
CREATE OR REPLACE FUNCTION format_name(
    p_locale TEXT,
    p_seed TEXT,
    p_batch_idx BIGINT,
    p_pos_in_batch BIGINT
)
RETURNS TABLE(full_name TEXT, out_gender TEXT)
LANGUAGE plpgsql AS $$
DECLARE
    base_seed TEXT := p_locale || '|' || p_seed || '|' || p_batch_idx;
    gender_pick TEXT;
    fname TEXT;
    lname TEXT;
    shuffled_first_ids BIGINT[];
    shuffled_last_ids BIGINT[];
    f_id BIGINT;
    l_id BIGINT;
BEGIN
    -- Gender
    gender_pick := CASE WHEN prng_uniform(base_seed || '|gender', p_pos_in_batch) < 0.5 THEN 'M' ELSE 'F' END;

    -- Filtered first names
    SELECT array_agg(n.id) INTO shuffled_first_ids
    FROM names n
    WHERE n.locale = p_locale
      AND n.name_type = 'first'
      AND (n.gender IS NULL OR n.gender = gender_pick);

    IF shuffled_first_ids IS NULL OR array_length(shuffled_first_ids,1) = 0 THEN
        RAISE WARNING 'No first names found for locale=% gender=%', p_locale, gender_pick;
        shuffled_first_ids := ARRAY[1];
    END IF;

    shuffled_first_ids := shuffle_ids(shuffled_first_ids, base_seed || '|fname');
    f_id := shuffled_first_ids[1 + (p_pos_in_batch % array_length(shuffled_first_ids,1))];
    SELECT n.value INTO fname FROM names n WHERE n.id = f_id;

    -- Filtered last names
    SELECT array_agg(n.id) INTO shuffled_last_ids
    FROM names n
    WHERE n.locale = p_locale
      AND n.name_type = 'last';

    IF shuffled_last_ids IS NULL OR array_length(shuffled_last_ids,1) = 0 THEN
        RAISE WARNING 'No last names found for locale=%', p_locale;
        shuffled_last_ids := ARRAY[1];
    END IF;

    shuffled_last_ids := shuffle_ids(shuffled_last_ids, base_seed || '|lname');
    l_id := shuffled_last_ids[1 + (p_pos_in_batch % array_length(shuffled_last_ids,1))];
    SELECT n.value INTO lname FROM names n WHERE n.id = l_id;

    full_name := COALESCE(fname,'John') || ' ' || COALESCE(lname,'Doe');
    out_gender := gender_pick;

    RETURN NEXT;
END
$$;

-- FORMAT ADDRESS
CREATE OR REPLACE FUNCTION format_address(
    p_locale TEXT,
    p_seed TEXT,
    p_batch_idx BIGINT,
    p_pos_in_batch BIGINT
)
RETURNS TABLE(address TEXT, out_city TEXT, out_postal TEXT, out_region TEXT)
LANGUAGE plpgsql AS $$
DECLARE
    base_seed TEXT := p_locale || '|' || p_seed || '|' || p_batch_idx || '|addr';
    s_id BIGINT;
    sf_id BIGINT;
    city_id BIGINT;
    street_name TEXT;
    street_suffix TEXT;
    city_name TEXT;
    region_name TEXT;
    postal TEXT;
    house_no INT;
    shuffled_street_ids BIGINT[];
    shuffled_suffix_ids BIGINT[];
    shuffled_city_ids BIGINT[];
BEGIN
    -- Streets
    SELECT array_agg(s.id) INTO shuffled_street_ids FROM street_names s WHERE s.locale = p_locale;
    shuffled_street_ids := shuffle_ids(shuffled_street_ids, base_seed || '|street');
    s_id := shuffled_street_ids[1 + (p_pos_in_batch % array_length(shuffled_street_ids,1))];
    SELECT s.name INTO street_name FROM street_names s WHERE s.id = s_id;

    -- Street suffixes
    SELECT array_agg(ss.id) INTO shuffled_suffix_ids FROM street_suffixes ss WHERE ss.locale = p_locale;
    shuffled_suffix_ids := shuffle_ids(shuffled_suffix_ids, base_seed || '|suffix');
    sf_id := shuffled_suffix_ids[1 + (p_pos_in_batch % array_length(shuffled_suffix_ids,1))];
    SELECT ss.suffix INTO street_suffix FROM street_suffixes ss WHERE ss.id = sf_id;

    -- Cities
    SELECT array_agg(c.id) INTO shuffled_city_ids FROM cities c WHERE c.locale = p_locale;
    shuffled_city_ids := shuffle_ids(shuffled_city_ids, base_seed || '|city');
    city_id := shuffled_city_ids[1 + (p_pos_in_batch % array_length(shuffled_city_ids,1))];
    SELECT c.city, c.region, c.postal_code INTO city_name, region_name, postal
    FROM cities c WHERE c.id = city_id;

    house_no := prng_int_range(base_seed, p_pos_in_batch, 1, 999);

    address := street_name || ' ' || street_suffix || ' ' || house_no;
    out_city := city_name;
    out_region := region_name;
    out_postal := postal;

    RETURN NEXT;
END
$$;


-- GENERATE BATCH
CREATE OR REPLACE FUNCTION generate_batch(
    p_locale TEXT,
    p_seed TEXT,
    p_batch_idx BIGINT,
    p_batch_size BIGINT
)
RETURNS TABLE(
    full_name TEXT,
    gender TEXT,
    address TEXT,
    city TEXT,
    postal_code TEXT,
    region TEXT,
    eye_color TEXT,
    phone TEXT,
    email TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    i BIGINT;
    name_rec RECORD;
    addr_rec RECORD;
    shuffled_eye_ids BIGINT[];
    shuffled_phone_ids BIGINT[];
    shuffled_email_ids BIGINT[];
    eye_id BIGINT;
    phone_id BIGINT;
    email_id BIGINT;
    eye_color_var TEXT;
    phone_fmt_var TEXT;
    email_domain_var TEXT;
BEGIN
    -- Eye colors
    SELECT array_agg(e.id) INTO shuffled_eye_ids FROM eye_colors e WHERE e.locale = p_locale;
    shuffled_eye_ids := shuffle_ids(shuffled_eye_ids, p_seed || '|eye');

    -- Phone formats
    SELECT array_agg(pf.id) INTO shuffled_phone_ids FROM phone_formats pf WHERE pf.locale = p_locale;
    shuffled_phone_ids := shuffle_ids(shuffled_phone_ids, p_seed || '|phone');

    -- Email domains
    SELECT array_agg(ed.id) INTO shuffled_email_ids FROM email_domains ed WHERE ed.locale = p_locale;
    shuffled_email_ids := shuffle_ids(shuffled_email_ids, p_seed || '|email');

    FOR i IN 0..(p_batch_size - 1) LOOP
        -- Name & address
        SELECT * INTO name_rec FROM format_name(p_locale, p_seed, p_batch_idx, i);
        SELECT * INTO addr_rec FROM format_address(p_locale, p_seed, p_batch_idx, i);

        full_name := name_rec.full_name;
        gender := name_rec.out_gender;
        address := addr_rec.address;
        city := addr_rec.out_city;
        postal_code := addr_rec.out_postal;
        region := addr_rec.out_region;

        -- Eye color
        eye_id := shuffled_eye_ids[1 + (i % array_length(shuffled_eye_ids,1))];
        SELECT e.color INTO eye_color_var FROM eye_colors e WHERE e.id = eye_id;
        IF eye_color_var IS NULL THEN eye_color_var := 'Brown'; END IF;

        -- Phone
        phone_id := shuffled_phone_ids[1 + (i % array_length(shuffled_phone_ids,1))];
        SELECT pf.format_pattern INTO phone_fmt_var FROM phone_formats pf WHERE pf.id = phone_id;
        IF phone_fmt_var IS NULL THEN phone_fmt_var := '+1-000-000-0000'; END IF;

        -- Email domain
        email_id := shuffled_email_ids[1 + (i % array_length(shuffled_email_ids,1))];
        SELECT ed.domain INTO email_domain_var FROM email_domains ed WHERE ed.id = email_id;
        IF email_domain_var IS NULL THEN email_domain_var := 'example.com'; END IF;

        eye_color := eye_color_var;
        phone := phone_fmt_var;
        email := lower(replace(full_name,' ','_')) || '@' || email_domain_var;

        RETURN NEXT;
    END LOOP;
END
$$;