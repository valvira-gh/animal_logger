WITH duplicates AS (
    SELECT id,
            ROW_NUMBER() OVER (PARTITION BY name, species, birth_date ORDER BY id) AS rnum
    FROM animals
)
DELETE FROM animals
WHERE id IN (
    SELECT id
    FROM duplicates
    WHERE rnum > 1
);