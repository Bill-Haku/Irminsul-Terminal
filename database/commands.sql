# insert or update user uid table
insert into UID_TABLE(user_id, uid, update_time)
values ('test', 'test', now())
on duplicate key update uid = 'test', update_time = now();

# update update_time
update UID_TABLE
set update_time = now()
where user_id = 'test';