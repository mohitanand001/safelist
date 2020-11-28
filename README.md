# safelist
Thread Safe list in python
works in 3 modes:<br>
**dirty:** Allows `concurrent` reads and `concurrent` writers to the access the list. No lock mode.<br>
**safe_write:** Allows exactly one writer at a time, but reader threads can access without
                having to acquire any lock. Possibility of dirty reads. Writers need an exclusive lock.
**safe_readwrite:** Allows either `exactly` one writer or `n` readers concurrently accessing. Readers and Writers 
                    both need to acquire the lock before accessing the list.
