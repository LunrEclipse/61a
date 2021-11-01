(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s))
    )

(define (caddr s) (car (cddr s))
)

(define (ordered? s) (if (null? (cdr s)) #t 
                         (if (< (cadr s) (car s) ) #f (ordered? (cdr s)) )
                         )
    )

(define (square x) (* x x))

(define (pow base exp) (cond
                           ( (= exp 1) base)
                           ( (= base 1) base)
                           ( (even? exp) (square (pow base (/ exp 2))))
                           (else (* base (pow base (- exp 1))))
                             )
    
    )
