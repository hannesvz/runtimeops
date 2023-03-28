from platformshconfig import Config
config = Config()

database_definitions = [
    {
        'name': 'records',
        'sql': '''CREATE TABLE `records` (
            `req_id` tinytext COLLATE utf8mb4_unicode_ci NOT NULL,
            `secret` tinytext COLLATE utf8mb4_unicode_ci NOT NULL,
            PRIMARY KEY (`req_id`(255))
        )
    COLLATE='utf8mb4_unicode_ci'
    ;'''
    }
]
