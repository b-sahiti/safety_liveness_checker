#define rand	pan_rand
#define pthread_equal(a,b)	((a)==(b))
#if defined(HAS_CODE) && defined(VERBOSE)
	#ifdef BFS_PAR
		bfs_printf("Pr: %d Tr: %d\n", II, t->forw);
	#else
		cpu_printf("Pr: %d Tr: %d\n", II, t->forw);
	#endif
#endif
	switch (t->forw) {
	default: Uerror("bad forward move");
	case 0:	/* if without executable clauses */
		continue;
	case 1: /* generic 'goto' or 'skip' */
		IfNotBlocked
		_m = 3; goto P999;
	case 2: /* generic 'else' */
		IfNotBlocked
		if (trpt->o_pm&1) continue;
		_m = 3; goto P999;

		 /* PROC :init: */
	case 3: // STATE 1 - fw.pml:19 - [(run A0())] (0:0:0 - 1)
		IfNotBlocked
		reached[2][1] = 1;
		if (!(addproc(II, 1, 0)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 4: // STATE 2 - fw.pml:20 - [(run A1())] (0:0:0 - 1)
		IfNotBlocked
		reached[2][2] = 1;
		if (!(addproc(II, 1, 1)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 5: // STATE 3 - fw.pml:21 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[2][3] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */

		 /* PROC A1 */
	case 6: // STATE 1 - fw.pml:14 - [((r1==1))] (0:0:0 - 1)
		IfNotBlocked
		reached[1][1] = 1;
		if (!((((int)now.r1)==1)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 7: // STATE 2 - fw.pml:14 - [r0 = 0] (0:0:1 - 1)
		IfNotBlocked
		reached[1][2] = 1;
		(trpt+1)->bup.oval = ((int)now.r0);
		now.r0 = 0;
#ifdef VAR_RANGES
		logval("r0", ((int)now.r0));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 8: // STATE 3 - fw.pml:14 - [r1 = 0] (0:0:1 - 1)
		IfNotBlocked
		reached[1][3] = 1;
		(trpt+1)->bup.oval = ((int)now.r1);
		now.r1 = 0;
#ifdef VAR_RANGES
		logval("r1", ((int)now.r1));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 9: // STATE 4 - fw.pml:14 - [r4 = 0] (0:0:1 - 1)
		IfNotBlocked
		reached[1][4] = 1;
		(trpt+1)->bup.oval = ((int)r4);
		r4 = 0;
#ifdef VAR_RANGES
		logval("r4", ((int)r4));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 10: // STATE 5 - fw.pml:15 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[1][5] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */

		 /* PROC A0 */
	case 11: // STATE 1 - fw.pml:10 - [((r0==1))] (0:0:0 - 1)
		IfNotBlocked
		reached[0][1] = 1;
		if (!((((int)now.r0)==1)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 12: // STATE 2 - fw.pml:10 - [r0 = 0] (0:0:1 - 1)
		IfNotBlocked
		reached[0][2] = 1;
		(trpt+1)->bup.oval = ((int)now.r0);
		now.r0 = 0;
#ifdef VAR_RANGES
		logval("r0", ((int)now.r0));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 13: // STATE 3 - fw.pml:10 - [r1 = 0] (0:0:1 - 1)
		IfNotBlocked
		reached[0][3] = 1;
		(trpt+1)->bup.oval = ((int)now.r1);
		now.r1 = 0;
#ifdef VAR_RANGES
		logval("r1", ((int)now.r1));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 14: // STATE 4 - fw.pml:10 - [r3 = 0] (0:0:1 - 1)
		IfNotBlocked
		reached[0][4] = 1;
		(trpt+1)->bup.oval = ((int)r3);
		r3 = 0;
#ifdef VAR_RANGES
		logval("r3", ((int)r3));
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 15: // STATE 5 - fw.pml:11 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[0][5] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */
	case  _T5:	/* np_ */
		if (!((!(trpt->o_pm&4) && !(trpt->tau&128))))
			continue;
		/* else fall through */
	case  _T2:	/* true */
		_m = 3; goto P999;
#undef rand
	}

