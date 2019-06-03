#lang scheme
;2014400054

;This function takes a single argument (a farm) and returns the transportation cost of crops from that farm.
(define (TRANSPORTATION-COST farm)
  (cond
   ( (null? (TCHELPER FARMS farm))
    0)
   (else
    (TCHELPER FARMS farm))))

(define (TCHELPER list farm)
  (cond
    ( (null? list)
    '() )
    (else
     (cond
       ( (equal? farm (car(car list))) (car(cdr ( car list))) )
       (else (TCHELPER (cdr list) farm))
       ))
    ))

;This function takes a single argument (a farm) and returns a list of available crops that are grown on that farm.
(define (AVAILABLE-CROPS farm) (ACHELPER FARMS farm))

(define (ACHELPER list farm)
  (cond
    ( (null? list)
    '() )
    (else
     (cond
       ( (equal? farm (car(car list))) (car(cdr(cdr(car list)))))
       (else (ACHELPER (cdr list) farm))
       ))
    ))

;This function takes a single argument (a customer) and returns a list involving his/her interested crops.
(define (INTERESTED-CROPS customer) (ICHELPER CUSTOMERS customer))

(define (ICHELPER list customer)
  (cond
    ((null? list)
    '() )
    (else
     (cond
       ( (equal? customer (car(car list))) (car(cdr(cdr(car list)))))
       (else (ICHELPER (cdr list) customer))
       ))
    ))

;This function takes a single argument (a customer) and returns a list farms that the customer has contract with.
(define (CONTRACT-FARMS customer) (CFHELPER CUSTOMERS customer))

(define (CFHELPER list customer)
  (cond
    ((null? list)
    '() )
    (else
     (cond
       ( (equal? customer (car(car list))) (car(cdr(car list))))
       (else (CFHELPER (cdr list) customer))
       ))
    ))

;This function takes a single argument (a farm) and returns a list of customers who has contract with that farm.
(define (CONTRACT-WITH-FARM farm) (CWFHELPER CUSTOMERS farm '()))

(define (CWFHELPER listAll farm list1)
  (cond
    ( (null? listAll)
      list1 )
   (else
    (cond
      ( (CHECKFARM farm (car(cdr(car listAll)))) (CWFHELPER (cdr listAll) farm (append list1(list(car(car listAll))))))
      (else (CWFHELPER (cdr listAll) farm list1))
      ))
   ))

(define (CHECKFARM farm list)
  (cond
    ( (null? list)
      #f)
    (else
     (cond
      ( (equal? farm (car list)) #t)
      (else (CHECKFARM farm (cdr list)))
      ))
    ))

;This function takes a single argument (a crop) and returns a list of customers who wants to buy that crop.
(define (INTERESTED-IN-CROP farm) (IICHELPER CUSTOMERS farm '()))

(define (IICHELPER listAll farm list1)
  (cond
    ( (null? listAll)
      list1 )
   (else
    (cond
      ( (CHECKCROP farm (car(cdr(cdr(car listAll))))) (IICHELPER (cdr listAll) farm (append list1(list(car(car listAll))))))
      (else (IICHELPER (cdr listAll) farm list1))
      ))
   ))

(define (CHECKCROP farm list)
  (cond
    ( (null? list)
      #f)
    (else
     (cond
      ( (equal? farm (car list)) #t)
      (else (CHECKCROP farm (cdr list)))
      ))
    ))

;This function  takes a single argument (a crop) and returns the minimum sale price for that crop.
(define (MIN-SALE-PRICE crop)(MSPHELPER CROPS crop '()))

(define (MSPHELPER listAll crop list1)
  (cond
    ((null? listAll)
      (cond
        ((null? list1)
          0)
        (else (findMin list1)
              )))
    (else
     (cond
       ( (equal? crop (car(car listAll))) (MSPHELPER (cdr listAll) crop (append list1(list(car(cdr(cdr( car listAll))))))))
       (else (MSPHELPER (cdr listAll) crop list1))
       ))
    ))

;This function finds min elements of list.
(define (findMin list)
  (if (null? (cdr list))
      (car list)
      (if (< (car list) (findMin (cdr list)))
          (car list)
          (findMin (cdr list)))))

;This function takes two arguments (a min price and a max price) and returns the list of crops which has sale price between these arguments, inclusive.
(define (CROPS-BETWEEN bigger smaller) (REMOVE-DUPLICATES (CBHELPER bigger smaller CROPS)))

(define (CBHELPER bigger smaller list)
  (cond
    ((eqv? list '()) '())
    (else
     (cond
      ((and(<= (car(cdr(cdr(car list)))) smaller) (>= (car(cdr(cdr(car list)))) bigger))
        (cons (car (car list)) (CBHELPER bigger smaller (cdr list))))
      (else
        (CBHELPER bigger smaller (cdr list)))))))

;This function takes one argument(a list) and returns the the list which do not have duplicate elements.
(define (REMOVE-DUPLICATES list)
  (cond ((null? list)
         '())
        ((member (car list) (cdr list))
         (REMOVE-DUPLICATES (cdr list)))
        (else
         (cons (car list) (REMOVE-DUPLICATES (cdr list))))))

;This function takes two arguments (a customer and a crop) and returns the minimum cost of buying that crop for the customer.  
(define (BUY-PRICE customer crop)
  (cond 
   ((null? (BPHELPER crop (CONTRACT-FARMS customer)))
   0)
   (else
    (findMin (BPHELPER crop (CONTRACT-FARMS customer))))
  )
)

(define (BPHELPER crop list)
  (cond
    ((eqv? list '()) '())
    (else
     (cond
       ((member crop (AVAILABLE-CROPS (car list)))
        (cons (+ (TRANSPORTATION-COST (car list)) (CPHELPER crop (car list) CROPS))
              (BPHELPER crop (cdr list))))
       (else
        (BPHELPER crop (cdr list)))))))

;This function takes three arguments(a crop, a farm and a list) and returns the cost of crops.
(define (CPHELPER crop farm list)
  (cond
    ((eqv? list '()) '0)
    (else
     (cond
       ((and(equal? crop (car (car list))) (equal? farm (cadr (car list))))
        (car(cdr(cdr(car list)))))
       (else
        (CPHELPER crop farm (cdr list)))))))

;This function takes a single argument (a customer) and returns the minimum total price for buying all the crops in the customers’ list.
(define (TOTAL-PRICE customer)(TPHELPER customer (INTERESTED-CROPS customer)))

(define (TPHELPER customer elemList)
  (if
   (null? elemList)
   0
   (+ (BUY-PRICE customer (car elemList)) (TPHELPER customer (cdr elemList)))
   )
  )