-- Pseudo-random number generator functions for deterministic data

-- Convert a text seed into a numeric hash safely
CREATE OR REPLACE FUNCTION prng_hash(seed TEXT)
RETURNS BIGINT
LANGUAGE plpgsql
AS $$
DECLARE
    h NUMERIC := 0;
    i INT;
    mod_val NUMERIC := 9223372036854775807; -- max bigint
BEGIN
    IF seed IS NULL THEN
        RETURN 0;
    END IF;

    FOR i IN 1..length(seed) LOOP
        h := mod((h * 31 + ascii(substr(seed,i,1))), mod_val);
    END LOOP;

    RETURN h::BIGINT;
END;
$$;

-- Uniform pseudo-random number between 0 and 1
CREATE OR REPLACE FUNCTION prng_uniform(seed TEXT, counter BIGINT)
RETURNS DOUBLE PRECISION
LANGUAGE plpgsql
AS $$
DECLARE
    x BIGINT;
BEGIN
    x := prng_hash(seed || '|' || counter);
    RETURN (x % 1000000)::DOUBLE PRECISION / 1000000;
END;
$$;

-- Uniform integer between min_val and max_val (inclusive)
CREATE OR REPLACE FUNCTION prng_int_range(seed TEXT, counter BIGINT, min_val BIGINT, max_val BIGINT)
RETURNS BIGINT
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN min_val + floor(prng_uniform(seed, counter) * (max_val - min_val + 1))::BIGINT;
END;
$$;

-- Uniform double between min_val and max_val
CREATE OR REPLACE FUNCTION prng_double_range(seed TEXT, counter BIGINT, min_val DOUBLE PRECISION, max_val DOUBLE PRECISION)
RETURNS DOUBLE PRECISION
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN min_val + prng_uniform(seed, counter) * (max_val - min_val);
END;
$$;

-- Normal distribution using Box-Muller transform
CREATE OR REPLACE FUNCTION prng_normal(seed TEXT, counter BIGINT, mean DOUBLE PRECISION, stddev DOUBLE PRECISION)
RETURNS DOUBLE PRECISION
LANGUAGE plpgsql
AS $$
DECLARE
    u1 DOUBLE PRECISION;
    u2 DOUBLE PRECISION;
BEGIN
    u1 := prng_uniform(seed || '|u1', counter);
    u2 := prng_uniform(seed || '|u2', counter);

    RETURN mean + stddev * sqrt(-2 * ln(u1 + 1e-10)) * cos(2 * pi() * u2);
END;
$$;