# safelist
Thread Safe list in python
works in 3 modes:<br>

**dirty**: Allows `concurrent` reads and `concurrent` writers to the access the list. No lock mode.<br>
**safe_write**: Allows exactly one writer at a time, but reader threads can access without
                having to acquire any lock. <br> Possibility of dirty reads. Writers need an exclusive lock. <br>
**safe_readwrite**: Allows either `exactly` one writer or `n` readers concurrently accessing.<br> Readers and Writers 
                    both need to acquire the lock before accessing the list.



This codebase provides an implementation of different types of lists with varying levels of thread safety for concurrent operations. The main goal is to demonstrate how you can create thread-safe data structures in Python using semaphores from the `threading` module.

Here's an explanation of the code:

1. **`safelist(mode="dirty")`**: This function is a factory function that returns an instance of one of three list types: `DirtyList`, `SafeWriteList`, or `SafeReadWriteList`. The `mode` parameter determines which type of list to create. If the mode is "dirty," it returns an instance of `DirtyList`, which is not thread-safe. If the mode is "safe_write," it returns an instance of `SafeWriteList`, which is thread-safe for write operations (push and modify). If the mode is "safe_readwrite," it returns an instance of `SafeReadWriteList`, which is thread-safe for both read and write operations.

2. **`BaseSafeList`**: This is an abstract base class that defines the common interface and some default behavior for all list types. It has methods for modifying, getting, and pushing elements into the list, but these methods are implemented to do nothing by default.

3. **`DirtyList`**: This class represents a non-thread-safe list. It inherits from `BaseSafeList` and simply uses a regular Python list (`self._lis`) to store data. The `push`, `modify`, and `get` methods directly operate on this list without any thread safety mechanisms.

4. **`SafeWriteList`**: This class represents a thread-safe list for write operations. It uses a semaphore (`self.s_writer`) to ensure that only one thread can write to the list at a time. The `push` and `modify` methods acquire the semaphore before performing their respective operations and release it afterward.

5. **`SafeReadWriteList`**: This class represents a thread-safe list for both read and write operations. It uses two semaphores: `self.s_readerwriter` to control write access and `self.s_readers` to count the number of concurrent readers. The `push` and `modify` methods acquire the `self.s_readerwriter` semaphore for exclusive write access. The `get` method allows multiple readers concurrently but acquires the `self.s_readerwriter` semaphore if it's the first reader and releases it when there are no more readers.

In summary, this codebase provides different types of lists with varying levels of thread safety. `DirtyList` is not thread-safe, `SafeWriteList` is thread-safe for write operations, and `SafeReadWriteList` is thread-safe for both read and write operations. It demonstrates how to use semaphores to control access to shared resources in a multi-threaded environment, ensuring data integrity and avoiding race conditions.
