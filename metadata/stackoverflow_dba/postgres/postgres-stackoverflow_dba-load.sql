\copy badges       from '../../LpBound/data/datasets/stackoverflow_dba/Badges.csv'      with (format csv, delimiter ',', quote '"', escape '"', null '');
\copy comments     from '../../LpBound/data/datasets/stackoverflow_dba/Comments.csv'    with (format csv, delimiter ',', quote '"', escape '"', null '');
\copy users        from '../../LpBound/data/datasets/stackoverflow_dba/Users.csv'       with (format csv, delimiter ',', quote '"', escape '"', null '');
\copy tags         from '../../LpBound/data/datasets/stackoverflow_dba/Tags.csv'        with (format csv, delimiter ',', quote '"', escape '"', null '');
\copy posts        from '../../LpBound/data/datasets/stackoverflow_dba/Posts.csv'       with (format csv, delimiter ',', quote '"', escape '"', null '');
\copy votes        from '../../LpBound/data/datasets/stackoverflow_dba/Votes.csv'       with (format csv, delimiter ',', quote '"', escape '"', null '');
\copy posthistory  from '../../LpBound/data/datasets/stackoverflow_dba/PostHistory.csv' with (format csv, delimiter ',', quote '"', escape '"', null '');
\copy postlinks    from '../../LpBound/data/datasets/stackoverflow_dba/PostLinks.csv'   with (format csv, delimiter ',', quote '"', escape '"', null '');