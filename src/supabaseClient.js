import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

// Esse objeto 'supabase' é o que usaremos para conversar com o banco
export const supabase = createClient(supabaseUrl, supabaseKey);