box.cfg{}
box.schema.user.passwd('pass')

-- Cache size
cache_size_space = box.schema.space.create('cache_size')
cache_size_space:format({
    {name = 'id', type = 'unsigned'},
    {name = 'size', type = 'unsigned'}
})

cache_size_space:create_index('id_index', {
    type = 'hash',
    parts = {'id'}
})

cache_size_space:insert({1, 0})

-- DisciplineWorkProgram
work_program_space = box.schema.space.create('discipline_work_program')

work_program_space:format({
    {name = 'id', type = 'unsigned'},
    {name = 'name', type = 'string'},
    {name = 'author', type = 'string'},
    {name = 'competency', type = 'string'}
})

work_program_space:create_index('id_index', {
    type = 'hash',
    parts = {'id'}
})

work_program_space:create_index('name_index', {
    type = 'tree',
    parts = {'name'},
    unique = false,
})

-- LearningOutcomes
learning_outcomes_space = box.schema.space.create('learning_outcomes')
learning_outcomes_space:format({
    {name = 'id', type = 'unsigned'},
    {name = 'discipline_id', type = 'unsigned'},
    {name = 'competency_code', type = 'string'},
    {name = 'formulation', type = 'string'},
    {name = 'results', type = 'string'},
    {name = 'formst_and_methods', type = 'string'}
})

learning_outcomes_space:create_index('id_index', {
    type = 'hash',
    parts = {'id'}
})

learning_outcomes_space:create_index('discipline_id_index', {
    type = 'tree',
    parts = {'discipline_id'},
    unique = false,
})

learning_outcomes_space:create_index('competency_index', {
    type = 'tree',
    parts = {'competency_code'},
    unique = false,
})

-- EducationalProgram
educational_program_space = box.schema.space.create('educational_program')
educational_program_space:format({
    {name = 'id', type = 'unsigned'},
    {name = 'name', type = 'string'}
})

educational_program_space:create_index('id_index', {
    type = 'hash',
    parts = {'id'}
})

educational_program_space:create_index('name_index', {
    type = 'tree',
    parts = {'name'},
    unique = false,
})

-- DisciplineScopeSemester
discipline_scope_semester_space = box.schema.space.create('discipline_scope_semester')
discipline_scope_semester_space:format({
    {name = 'id', type = 'unsigned'},
    {name = 'discipline_id', type = 'unsigned'},
    {name = 'semester_number', type = 'unsigned'},
    {name = 'credit_units', type = 'unsigned'},
    {name = 'total_hours', type = 'unsigned'},
    {name = 'lectures_hours', type = 'unsigned'},
    {name = 'seminars_hours', type = 'unsigned'},
    {name = 'laboratory_work_hours', type = 'unsigned'},
    {name = 'independent_work_hours', type = 'unsigned'},
    {name = 'certification_type', type = 'string'}
})

discipline_scope_semester_space:create_index('id_index', {
    type = 'hash',
    parts = {'id'}
})

discipline_scope_semester_space:create_index('discipline_id_index', {
    type = 'tree',
    parts = {'discipline_id'},
    unique = false,
})

discipline_scope_semester_space:create_index('certification_index', {
    type = 'tree',
    parts = {'certification_type'},
    unique = false,
})

-- DisciplineModule
discipline_module_space = box.schema.space.create('discipline_module')
discipline_module_space:format({
    {name = 'id', type = 'unsigned'},
    {name = 'discipline_id', type = 'unsigned'},
    {name = 'name', type = 'string'},
    {name = 'semester_number', type = 'unsigned'},
    {name = 'lectures_hours', type = 'unsigned'},
    {name = 'seminars_hours', type = 'unsigned'},
    {name = 'laboratory_work_hours', type = 'unsigned'},
    {name = 'independent_work_hours', type = 'unsigned'},
    {name = 'min_scores', type = 'unsigned'},
    {name = 'max_scores', type = 'unsigned'},
    {name = 'competency_code', type = 'string'}
})

discipline_module_space:create_index('id_index', {
    type = 'hash',
    parts = {'id'}
})

discipline_module_space:create_index('discipline_id_index', {
    type = 'tree',
    parts = {'discipline_id'},
    unique = false,
})

discipline_module_space:create_index('competency_index', {
    type = 'tree',
    parts = {'competency_code'},
    unique = false,
})

-- DisciplineMaterial
discipline_material_space = box.schema.space.create('discipline_material')
discipline_material_space:format({
    {name = 'id', type = 'unsigned'},
    {name = 'discipline_id', type = 'unsigned'},
    {name = 'marerial', type = 'string'}
})

discipline_material_space:create_index('id_index', {
    type = 'tree',
    parts = {'id'}
})

discipline_material_space:create_index('discipline_id_index', {
    type = 'tree',
    parts = {'discipline_id'},
    unique = false,
})