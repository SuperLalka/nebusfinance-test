
--
-- Name: public.check_activity_nested_level; Type: FUNCTION; Schema: public; Owner: debug
--

CREATE OR REPLACE FUNCTION public.check_activity_nested_level()
RETURNS trigger
AS $$
BEGIN
    IF EXISTS(
            select a3.* from public.activity a1
            join public.activity a2 on a1.activity_id = a2.id
            join public.activity a3 on a2.activity_id = a3.id
            where a1.id = NEW.activity_id
        )
        then RAISE EXCEPTION 'Maximum nesting level exceeded';
    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;


--
-- Name: check_activity_insert_trigger; Type: TRIGGER; Schema: public; Owner: debug
--

CREATE OR REPLACE TRIGGER check_activity_insert_trigger
    BEFORE INSERT
    ON public.activity
    FOR EACH ROW
    EXECUTE PROCEDURE public.check_activity_nested_level();
