box.session.user('admin')

local function sleep(n)
    os.execute("sleep " .. tonumber(n))
end

local function get_query_string(space)
    local cache_tuples = work_program_space:select()
    local query = "SELECT * FROM " .. space.name .. " WHERE "
    for _, tuple in ipairs(work_program_space) do
        query = "id = " .. tuple[1] " AND "
    end

    return query:sub(1, -5)
end

local function update_work_program_tuples(conn)
    local space = box.space.work_program_space
    local pg_tuples = conn:execute(get_query_string(space))
    space.replace(pg_tuples)
end

local function update_learning_outcomes_tuples(conn)
    local space = box.space.learning_outcomes
    local pg_tuples = conn:execute(get_query_string(space))
    space.replace(pg_tuples)
end

local function update_discipline_scope_tuples(conn)
    local space = box.space.disicipline_scope_semester
    local pg_tuples = conn:execute(get_query_string(space))
    space.replace(pg_tuples)
end

local function update_discipline_module_tuples(conn)
    local space = box.space.discipline_module
    local pg_tuples = conn:execute(get_query_string(space))
    space.replace(pg_tuples)
end

local function update_discipline_material_tuples(conn)
    local space = box.space.disicipline_material
    local pg_tuples = conn:execute(get_query_string(space))
    space.replace(pg_tuples)
end

box.ctl.on_schema_init(function()
    local log = require('log')
    log.info("On schema init triggered")
    sleep(1)

    local pg = require('pg')
    local conn = pg.connect({
        host = os.getenv('POSTGRES_HOST'),
        user = os.getenv('POSTGRES_USER'),
        pass = os.getenv('POSTGRES_PASSWORD'),
        db = os.getenv('POSTGRESS_DB'),
    })

    if conn == nil then
        log.error('Failed to connect to PSQL storage')
    end

    box.space.work_program_space:after_replace(update_work_program_tuples(conn))
    box.space.learning_outcomes:after_replace(update_learning_outcomes_tuples(conn))
    box.space.disicipline_scope_semester:after_replace(update_discipline_scope_tuples(conn))
    box.space.disicipline_module:after_replace(update_discipline_module_tuples(conn))
    box.space.disicipline_material:after_replace(update_discipline_material_tuples(conn))
end)

box.cfg{}