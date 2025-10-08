# -*- encoding: utf-8 -*-
'''
@文件        :performance_tools.py
@说明        :性能优化工具模块
@时间        :2024/01/01 00:00:00
@作者        :awx1192780
@版本        :1.0 - 性能优化工具
'''

import time
import functools
import psutil
import os
from typing import Callable, Any


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.start_time = None
        self.start_memory = None
    
    def start(self):
        """开始监控"""
        self.start_time = time.time()
        self.start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
    
    def stop(self):
        """停止监控并返回性能数据"""
        if self.start_time is None:
            return None
        
        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
        
        return {
            'execution_time': end_time - self.start_time,
            'memory_used': end_memory - self.start_memory,
            'peak_memory': end_memory
        }


def performance_monitor(func: Callable) -> Callable:
    """性能监控装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        monitor = PerformanceMonitor()
        monitor.start()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            stats = monitor.stop()
            if stats:
                print(f"函数 {func.__name__} 执行时间: {stats['execution_time']:.2f}秒, "
                      f"内存使用: {stats['memory_used']:.2f}MB")
    
    return wrapper


def batch_process(items, batch_size=100, processor=None):
    """
    批量处理数据，减少内存占用
    @param items: 要处理的数据项
    @param batch_size: 批处理大小
    @param processor: 处理函数
    """
    if processor is None:
        processor = lambda x: x
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield processor(batch)


class MemoryOptimizer:
    """内存优化器"""
    
    @staticmethod
    def optimize_string_operations(strings):
        """优化字符串操作"""
        # 使用生成器表达式而不是列表推导式
        return (s.strip() for s in strings if s)
    
    @staticmethod
    def optimize_dict_operations(dict_list):
        """优化字典操作"""
        # 使用字典推导式
        return {k: v for d in dict_list for k, v in d.items()}
    
    @staticmethod
    def clear_cache():
        """清理缓存"""
        import gc
        gc.collect()


def cache_result(maxsize=128):
    """结果缓存装饰器"""
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            if len(cache) >= maxsize:
                # 简单的LRU策略：删除最旧的项
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            cache[key] = result
            return result
        
        return wrapper
    return decorator


def optimize_file_reading(file_path, chunk_size=8192):
    """
    优化文件读取，使用分块读取
    @param file_path: 文件路径
    @param chunk_size: 块大小
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total, desc="处理中"):
        self.total = total
        self.current = 0
        self.desc = desc
        self.start_time = time.time()
    
    def update(self, increment=1):
        """更新进度"""
        self.current += increment
        if self.current % 10 == 0 or self.current == self.total:
            elapsed = time.time() - self.start_time
            rate = self.current / elapsed if elapsed > 0 else 0
            eta = (self.total - self.current) / rate if rate > 0 else 0
            
            print(f"\r{self.desc}: {self.current}/{self.total} "
                  f"({self.current/self.total*100:.1f}%) "
                  f"速度: {rate:.1f}项/秒 ETA: {eta:.1f}秒", end='')
    
    def finish(self):
        """完成进度跟踪"""
        elapsed = time.time() - self.start_time
        print(f"\n{self.desc}完成! 总耗时: {elapsed:.2f}秒")
