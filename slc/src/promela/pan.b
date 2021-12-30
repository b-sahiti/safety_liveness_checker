	switch (t->back) {
	default: Uerror("bad return move");
	case  0: goto R999; /* nothing to undo */

		 /* PROC :init: */

	case 3: // STATE 1
		;
		;
		delproc(0, now._nr_pr-1);
		;
		goto R999;

	case 4: // STATE 2
		;
		;
		delproc(0, now._nr_pr-1);
		;
		goto R999;

	case 5: // STATE 3
		;
		p_restor(II);
		;
		;
		goto R999;

		 /* PROC A1 */
;
		;
		
	case 7: // STATE 2
		;
		now.r0 = trpt->bup.oval;
		;
		goto R999;

	case 8: // STATE 3
		;
		now.r1 = trpt->bup.oval;
		;
		goto R999;

	case 9: // STATE 4
		;
		r4 = trpt->bup.oval;
		;
		goto R999;

	case 10: // STATE 5
		;
		p_restor(II);
		;
		;
		goto R999;

		 /* PROC A0 */
;
		;
		
	case 12: // STATE 2
		;
		now.r0 = trpt->bup.oval;
		;
		goto R999;

	case 13: // STATE 3
		;
		now.r1 = trpt->bup.oval;
		;
		goto R999;

	case 14: // STATE 4
		;
		r3 = trpt->bup.oval;
		;
		goto R999;

	case 15: // STATE 5
		;
		p_restor(II);
		;
		;
		goto R999;
	}

