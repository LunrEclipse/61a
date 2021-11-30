(define (split-at lst n)
    (cons (before lst n) (after lst n))
)

(define (before lst n)
    (if (null? lst)
        lst
        ( if(= n 0)
          nil
          (cons (car lst) (before (cdr lst) (- n 1)))
        )
    )
)

(define (after lst n)
    (if (null? lst)
        lst
        ( if(= n 0)
          lst
          (after (cdr lst) (- n 1))
        )
    )
)


(define (compose-all funcs)
    (lambda (n)
        (if (null? funcs)
            n
            ((compose-all (cdr funcs)) ((car funcs) n))
        )
    )
)
